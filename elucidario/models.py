"""Canonical data model for the structured corpus (Portuguese master text)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

BlockType = Literal[
    "paragraph", "heading", "quote", "verse", "list_item", "table", "bibliography", "xref", "note"
]


class Inline(BaseModel):
    """A styled span inside a block's text: [start, end) offsets."""

    start: int
    end: int
    style: Literal["italic", "bold", "small", "bold_italic"]


class Block(BaseModel):
    id: str  # "<article_id>#b012"
    type: BlockType
    level: int = 0  # heading depth (1 = section, 2 = subsection); list nesting
    text: str
    inlines: list[Inline] = Field(default_factory=list)
    lines: list[str] | None = None  # verse lines / table rows
    cells: list[list[str]] | None = None  # table cells when they can be recovered
    sentences: list[tuple[int, int]] = Field(default_factory=list)
    pages: list[int] = Field(default_factory=list)  # PDF pages the block spans
    printed_pages: list[int | None] = Field(default_factory=list)
    update_notes: list[str] = Field(default_factory=list)  # "(1921)", "(1940)" markers inside the block


class Article(BaseModel):
    id: str
    seq: int
    legacy_id: int | None = None
    headword: str
    headword_raw: str | None = None
    main: str
    qualifier: str | None = None
    sort_key: str
    volume: int
    pages: list[int | None]
    printed_pages: list[int | None]
    kind: Literal["article", "cross_reference", "compound", "front_matter"]
    parent_id: str | None = None
    children: list[str] = Field(default_factory=list)
    redirect_to: list[str] = Field(default_factory=list)  # raw targets from "V. X" for cross-references
    detected_by: str
    blocks: list[Block]
    formatting: dict[str, int] = Field(default_factory=dict)
    chars: int = 0
