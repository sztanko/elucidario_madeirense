"""Thin wrapper around the Message Batches API with a persistent job file, cost ledger and budget guard.

Usage:
    job = BatchJob("ocr_proof")                 # state in data/batches/ocr_proof/
    job.submit(requests, budget_usd=15)         # requests: list[{"custom_id": str, "params": {...}}]
    job.wait()                                  # polls until every batch has ended
    for custom_id, message in job.results(): ...
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from elucidario.llm.client import client
from elucidario.paths import DATA

# USD per million tokens, standard (non-batch) rates; batch = 50%.
PRICES = {
    "claude-opus-5-5": {"in": 4.0, "out": 20.0, "cache_read": 0.20, "cache_write": 5.0},
    "claude-sonnet-5": {"in": 2.0, "out": 10.0, "cache_read": 0.20, "cache_write": 2.5},
    "claude-haiku-4-5": {"in": 1.0, "out": 5.0, "cache_read": 0.10, "cache_write": 1.25},
    "claude-fable-5-1": {"in": 10.0, "out": 50.0, "cache_read": 0.25, "cache_write": 12.5},
}
BATCH_DISCOUNT = 0.5
MAX_PER_BATCH = 10_000
LEDGER = DATA / "ledger.jsonl"


def cost_usd(model: str, usage, batch: bool = True) -> float:
    p = PRICES.get(model) or next(v for k, v in PRICES.items() if model.startswith(k))
    u = usage if isinstance(usage, dict) else usage.model_dump()
    cc = u.get("cache_creation") or {}
    w1h = cc.get("ephemeral_1h_input_tokens") or 0
    w5m = (u.get("cache_creation_input_tokens") or 0) - w1h
    c = (
        u.get("input_tokens", 0) * p["in"]
        + u.get("output_tokens", 0) * p["out"]
        + (u.get("cache_read_input_tokens") or 0) * p["cache_read"]
        + w5m * p["cache_write"]
        + w1h * p["in"] * 2
    ) / 1e6
    return c * (BATCH_DISCOUNT if batch else 1.0)


def estimate_usd(model: str, input_tokens: int, output_tokens: int, batch: bool = True) -> float:
    return cost_usd(model, {"input_tokens": input_tokens, "output_tokens": output_tokens}, batch)


class BatchJob:
    def __init__(self, name: str):
        self.name = name
        self.dir = DATA / "batches" / name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"batches": []}

    def _save(self) -> None:
        self.state_path.write_text(json.dumps(self.state, indent=1))

    @property
    def submitted_ids(self) -> set[str]:
        ids = set()
        for b in self.state["batches"]:
            ids.update(b["custom_ids"])
        return ids

    def warm(self, requests: list[dict]) -> float:
        """Write the shared prefix to the prompt cache before submitting (parallel batch requests otherwise all miss).

        One synchronous request per distinct (model, system) prefix, with the smallest possible body. Returns USD spent.
        """
        seen, usd = set(), 0.0
        for r in requests:
            p = r["params"]
            key = (p["model"], json.dumps(p.get("system"), sort_keys=True, ensure_ascii=False))
            if key in seen or not p.get("system"):
                continue
            seen.add(key)
            q = {k: v for k, v in p.items() if k not in ("messages", "max_tokens")}
            q["messages"] = [{"role": "user", "content": "Cache warm-up: reply with an empty result."}]
            q["max_tokens"] = 2048
            try:
                with client().messages.stream(**q) as st:
                    m = st.get_final_message()
                usd += cost_usd(m.model, m.usage.model_dump(), batch=False)
            except Exception as ex:  # warm-up is best-effort
                print(f"{self.name}: warm-up failed: {ex}")
        return usd

    def submit(self, requests: list[dict], budget_usd: float, est_usd: float | None = None, warm: bool = True) -> list[str]:
        """Submit requests whose custom_id was not submitted before. Refuses if the estimate exceeds the budget."""
        todo = [r for r in requests if r["custom_id"] not in self.submitted_ids]
        if not todo:
            return []
        if warm and len(todo) > 5:
            for r in todo:  # 1-hour TTL so the warmed prefix outlives batch queueing
                for blk in r["params"].get("system") or []:
                    if isinstance(blk, dict) and blk.get("cache_control"):
                        blk["cache_control"] = {"type": "ephemeral", "ttl": "1h"}
            spent = self.warm(todo)
            with open(LEDGER, "a") as f:
                f.write(json.dumps({"job": self.name, "batch": "warm-up", "usd": round(spent, 4),
                                    "at": datetime.now(timezone.utc).isoformat()}) + "\n")
        if est_usd is not None and est_usd > budget_usd:
            raise RuntimeError(f"{self.name}: estimated ${est_usd:.2f} exceeds budget ${budget_usd:.2f}")
        ids = []
        for i in range(0, len(todo), MAX_PER_BATCH):
            chunk = todo[i : i + MAX_PER_BATCH]
            b = client().messages.batches.create(requests=chunk)
            self.state["batches"].append(
                {"id": b.id, "created": datetime.now(timezone.utc).isoformat(), "custom_ids": [r["custom_id"] for r in chunk]}
            )
            self._save()
            ids.append(b.id)
        return ids

    def wait(self, poll: int = 60, verbose: bool = True) -> None:
        while True:
            pending = []
            for b in self.state["batches"]:
                if b.get("ended"):
                    continue
                info = client().messages.batches.retrieve(b["id"])
                if info.processing_status == "ended":
                    b["ended"] = True
                    b["counts"] = info.request_counts.model_dump()
                    self._save()
                else:
                    pending.append((b["id"], info.request_counts.model_dump()))
            if not pending:
                return
            if verbose:
                print(f"[{datetime.now():%H:%M:%S}] {self.name}: waiting on {pending}", flush=True)
            time.sleep(poll)

    def results(self):
        """Yield (custom_id, result) for every ended batch; caches raw results to disk; records cost once."""
        for b in self.state["batches"]:
            if not b.get("ended"):
                continue
            path = self.dir / f"{b['id']}.jsonl"
            if not path.exists():
                with open(path, "w") as f:
                    for r in client().messages.batches.results(b["id"]):
                        f.write(r.model_dump_json() + "\n")
            if not b.get("costed"):
                total = 0.0
                for line in open(path):
                    r = json.loads(line)
                    if r["result"]["type"] == "succeeded":
                        m = r["result"]["message"]
                        total += cost_usd(m["model"], m["usage"])
                with open(LEDGER, "a") as f:
                    f.write(json.dumps({"job": self.name, "batch": b["id"], "usd": round(total, 4),
                                        "at": datetime.now(timezone.utc).isoformat()}) + "\n")
                b["costed"] = True
                b["usd"] = round(total, 4)
                self._save()
            for line in open(path):
                r = json.loads(line)
                yield r["custom_id"], r["result"]

    def spent(self) -> float:
        return sum(b.get("usd", 0.0) for b in self.state["batches"])


def message_text(result: dict) -> str | None:
    if result.get("type") != "succeeded":
        return None
    for block in result["message"]["content"]:
        if block["type"] == "text":
            return block["text"]
    return None
