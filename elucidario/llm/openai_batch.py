"""Minimal OpenAI Batch API runner (Responses endpoint) mirroring llm/batch.BatchJob, for benchmarking."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone

import httpx

from elucidario.llm.client import load_env
from elucidario.paths import DATA

API = "https://api.openai.com/v1"
PRICES = {  # USD / 1M tokens, Batch API (developers.openai.com/api/docs/pricing, 2026-09-27)
    "gpt-5.6-sol": {"in": 2.0, "cached": 0.20, "out": 10.0},
    "gpt-6-sol": {"in": 1.0, "cached": 0.10, "out": 5.0},
}
LEDGER = DATA / "ledger.jsonl"


def _h() -> dict:
    load_env()
    return {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}


def to_openai(anthropic_params: dict, effort: str | None) -> dict:
    """Convert our Anthropic request params into a /v1/responses body (same system, message and JSON schema)."""
    sys = "\n\n".join(b["text"] for b in anthropic_params["system"]) if isinstance(anthropic_params["system"], list) else anthropic_params["system"]
    fmt = anthropic_params["output_config"]["format"]
    body = {
        "model": anthropic_params["model"],
        "input": [{"role": "developer", "content": sys}] + [
            {"role": m["role"], "content": m["content"]} for m in anthropic_params["messages"]],
        "text": {"format": {"type": "json_schema", "name": "out", "schema": fmt["schema"], "strict": True}},
        "max_output_tokens": anthropic_params.get("max_tokens", 32000),
    }
    if effort:
        body["reasoning"] = {"effort": effort}
    return body


def cost(model: str, usage: dict) -> float:
    p = PRICES[model]
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens") or 0
    return ((usage["input_tokens"] - cached) * p["in"] + cached * p["cached"] + usage["output_tokens"] * p["out"]) / 1e6


class OpenAIBatch:
    def __init__(self, name: str):
        self.dir = DATA / "batches" / f"openai_{name}"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.name = name
        self.state_path = self.dir / "state.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {}

    def _save(self):
        self.state_path.write_text(json.dumps(self.state, indent=1))

    def submit(self, requests: list[dict]) -> str:
        if self.state.get("batch_id"):
            return self.state["batch_id"]
        path = self.dir / "input.jsonl"
        with open(path, "w") as f:
            for r in requests:
                f.write(json.dumps({"custom_id": r["custom_id"], "method": "POST", "url": "/v1/responses", "body": r["body"]},
                                   ensure_ascii=False) + "\n")
        up = httpx.post(f"{API}/files", headers=_h(), files={"file": ("input.jsonl", open(path, "rb"))},
                        data={"purpose": "batch"}, timeout=300).json()
        if "id" not in up:
            raise RuntimeError(f"OpenAI file upload failed: {up}")
        b = httpx.post(f"{API}/batches", headers=_h(), json={"input_file_id": up["id"], "endpoint": "/v1/responses",
                                                              "completion_window": "24h"}, timeout=60).json()
        if "id" not in b:
            raise RuntimeError(f"OpenAI batch creation failed: {b}")
        self.state.update(batch_id=b["id"], file_id=up["id"], created=datetime.now(timezone.utc).isoformat(), n=len(requests))
        self._save()
        return b["id"]

    def status(self) -> dict:
        return httpx.get(f"{API}/batches/{self.state['batch_id']}", headers=_h(), timeout=60).json()

    def wait(self, poll: int = 60) -> dict:
        while True:
            s = self.status()
            if s["status"] in ("completed", "failed", "expired", "cancelled"):
                return s
            time.sleep(poll)

    def results(self) -> dict[str, dict]:
        out_path = self.dir / "output.jsonl"
        if not out_path.exists():
            s = self.status()
            content = httpx.get(f"{API}/files/{s['output_file_id']}/content", headers=_h(), timeout=600).text
            out_path.write_text(content)
        res, usd = {}, 0.0
        for line in open(out_path):
            r = json.loads(line)
            body = (r.get("response") or {}).get("body") or {}
            if not body.get("output"):
                continue
            text = next((c["text"] for o in body["output"] if o.get("type") == "message" for c in o["content"]
                         if c.get("type") == "output_text"), None)
            res[r["custom_id"]] = {"text": text, "usage": body.get("usage"), "model": body.get("model")}
            if body.get("usage"):
                usd += cost(self.state_model(), body["usage"])
        if not self.state.get("costed"):
            with open(LEDGER, "a") as f:
                f.write(json.dumps({"job": f"openai_{self.name}", "batch": self.state["batch_id"], "usd": round(usd, 4),
                                    "at": datetime.now(timezone.utc).isoformat()}) + "\n")
            self.state.update(costed=True, usd=round(usd, 4))
            self._save()
        return res

    def state_model(self) -> str:
        return self.state.get("model") or ""
