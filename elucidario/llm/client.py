"""Anthropic client factory: loads .env and adds the workspace header when the key needs one."""

from __future__ import annotations

import os
from functools import lru_cache

import anthropic

from elucidario.paths import ROOT


def load_env() -> None:
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@lru_cache(maxsize=1)
def client() -> anthropic.Anthropic:
    load_env()
    headers = {}
    if ws := os.environ.get("ANTHROPIC_WORKSPACE_ID"):
        headers["anthropic-workspace-id"] = ws
    return anthropic.Anthropic(default_headers=headers, max_retries=5)
