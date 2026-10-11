"""Phase 4c: structure tables into typed cells.

Candidates: blocks typed `table`, plus multi-line blocks where most lines end in a number.
Opus (Batch API) returns the true block type and, for tables, caption, typed columns and verbatim cells.
Code verifies every cell against the source text, resolves ditto marks and parses numbers (elucidario.numbers).

Output: data/04_structured/tables.jsonl  {block_id, actual_type, caption, columns, header_rows, rows, parsed, issues}
The structure stage merges this file into the blocks (block.table, and block.type corrected).
"""

from __future__ import annotations

import json
import re

from elucidario.llm.batch import BatchJob, message_text
from elucidario.numbers import parse
from elucidario.paths import DATA

ART = DATA / "04_structured" / "articles.jsonl"
OUT = DATA / "04_structured" / "tables.jsonl"
MODEL = "claude-opus-5-5"
JOB = "tables"
DITTO = {'"', "»", "«", "*", "idem", "id.", "”", "“", "''", "〃"}
KINDS = ["label", "text", "year", "year_range", "date", "count", "weight", "volume", "length", "area", "money_reis",
         "money_escudos", "contos", "percent", "decimal", "temperature", "pressure", "other_number"]

SYSTEM = """You structure tables from the *Elucidário Madeirense* (Portuguese encyclopedia of Madeira, 1921/1940). The
text was OCR'd and typeset from a book; table columns survive only as line breaks, dot leaders (........) and spacing.

For each block decide `actual_type`: "table" (rows × columns of data), "list" (an enumeration, e.g. names with years in
running lines), "prose" (ordinary paragraph that merely has short lines), or "verse".
For tables return:
- `caption`: the table's title if it is inside the block (verbatim), else null;
- `columns`: one entry per column, `name_pt` (the header as printed, or a short Portuguese description if there is no
  printed header, e.g. "Ano", "Quantidade"), `kind` (see enum) and `unit` (as printed: "quilog.", "litros", "réis",
  "habitantes", "%", or null);
- `header_rows`: printed header rows as lists of verbatim strings (may be empty);
- `rows`: data rows, each a list of cells, one per column. Cells must be VERBATIM substrings of the block text (drop
  only dot leaders). Keep ditto marks (\", », *, idem) as they are. If a printed line holds two series side by side
  (e.g. "Março....763,60 Setembro....763,46"), make one row per series item (Março 763,60; Setembro 763,46), in reading
  order. Use "" for an empty cell.
Old number notation: "1:053:000" = 1,053,000; "20$000 réis" = 20,000 réis; "$28" (after 1911) = 28 centavos — keep
cells verbatim anyway; only choose the right column kind. Do not correct numbers."""

SCHEMA = {
    "type": "object",
    "properties": {"blocks": {"type": "array", "items": {"type": "object", "properties": {
        "block_id": {"type": "string"},
        "actual_type": {"type": "string", "enum": ["table", "list", "prose", "verse"]},
        "caption": {"type": ["string", "null"]},
        "columns": {"type": "array", "items": {"type": "object", "properties": {
            "name_pt": {"type": "string"}, "kind": {"type": "string", "enum": KINDS}, "unit": {"type": ["string", "null"]}},
            "required": ["name_pt", "kind", "unit"], "additionalProperties": False}},
        "header_rows": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        "rows": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
    }, "required": ["block_id", "actual_type", "caption", "columns", "header_rows", "rows"], "additionalProperties": False}}},
    "required": ["blocks"], "additionalProperties": False,
}


def candidates() -> list[dict]:
    out = []
    for line in open(ART):
        a = json.loads(line)
        prev_text = ""
        for b in a["blocks"]:
            lines = b.get("lines") or []
            is_cand = b["type"] == "table"
            if not is_cand and b["type"] in ("verse", "paragraph") and lines and len(lines) >= 4:
                numeric_end = sum(1 for l in lines if re.search(r"\d[\d.,:$%]*\s*[\"»]?\s*$", l))
                is_cand = numeric_end >= 0.6 * len(lines)
            if is_cand:
                out.append({"block_id": b["id"], "headword": a["headword"], "type": b["type"],
                            "lines": lines or [b["text"]], "before": prev_text[-300:]})
            prev_text = b["text"]
    return out


def submit(budget_usd: float = 3.0) -> dict:
    cands = candidates()
    reqs = []
    for i in range(0, len(cands), 4):
        chunk = cands[i: i + 4]
        body = "\n\n".join(
            f"=== block_id={c['block_id']} (entry: {c['headword']})\nPreceding text: …{c['before']}\nBlock lines:\n" + "\n".join(c["lines"])
            for c in chunk)
        reqs.append({"custom_id": f"tb{i // 4:04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": body + f"\n\nReturn all {len(chunk)} blocks."}],
            "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        }})
    ids = BatchJob(JOB).submit(reqs, budget_usd=budget_usd, est_usd=None)
    return {"candidates": len(cands), "requests": len(reqs), "batches": ids}


def squash(s: str) -> str:
    return re.sub(r"\s+|\.{3,}", "", s)


KIND_UNIT = {"weight": "kg", "volume": "l", "length": "m", "area": "ha", "money_reis": "réis", "money_escudos": "escudos",
             "contos": "contos", "percent": "%"}


def parse_cell(cell: str, kind: str) -> dict | str:
    if kind in ("label", "text", "date", "year_range") or not re.search(r"\d", cell):
        return cell
    ns = parse(cell)
    if len(ns) != 1:
        return {"raw": cell, "numbers": [n.to_json() for n in ns]} if ns else cell
    n = ns[0].to_json()
    if kind == "money_reis" and n["kind"] == "integer":
        n["kind"], n["unit"] = "money_reis", "réis"
    elif kind == "contos" and n["kind"] == "integer":
        n["kind"], n["unit"] = "contos", "contos"
    elif kind in KIND_UNIT and not n.get("unit"):
        n["unit"] = KIND_UNIT[kind]
    if kind == "year":
        n["kind"] = "year"
    n["cell"] = cell
    return n


def collect() -> dict:
    cands = {c["block_id"]: c for c in candidates()}
    rows_out, stats = [], {"tables": 0, "list": 0, "prose": 0, "verse": 0, "cells": 0, "unverified_cells": 0, "ditto": 0}
    for cid, res in BatchJob(JOB).results():
        t = message_text(res)
        if not t:
            continue
        for blk in json.loads(t)["blocks"]:
            c = cands.get(blk["block_id"])
            if not c:
                continue
            stats[blk["actual_type"] if blk["actual_type"] != "table" else "tables"] += 1
            if blk["actual_type"] != "table":
                rows_out.append({"block_id": blk["block_id"], "actual_type": blk["actual_type"]})
                continue
            source = squash(" ".join(c["lines"]))
            issues = []
            parsed, prev = [], None
            ncol = len(blk["columns"])
            for r in blk["rows"]:
                r = (r + [""] * ncol)[:ncol] if ncol else r
                out_row = []
                for j, cell in enumerate(r):
                    stats["cells"] += 1
                    if cell and squash(cell) not in source:
                        issues.append(f"cell not in source: {cell!r}")
                        stats["unverified_cells"] += 1
                    kind = blk["columns"][j]["kind"] if j < ncol else "text"
                    if cell.strip().lower() in DITTO and prev is not None and j < len(prev):
                        stats["ditto"] += 1
                        above = prev[j]
                        out_row.append({"ditto": cell, "same_as": above} if isinstance(above, (dict, str)) else cell)
                    else:
                        out_row.append(parse_cell(cell, kind))
                parsed.append(out_row)
                prev = [x.get("same_as", x) if isinstance(x, dict) and "ditto" in x else x for x in out_row]
            rows_out.append({**blk, "parsed": parsed, "issues": issues})
    with open(OUT, "w") as f:
        for r in rows_out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    stats["usd"] = round(BatchJob(JOB).spent(), 2)
    return stats
