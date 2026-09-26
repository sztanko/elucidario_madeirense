"""Pydantic schema for per-article enrichment (Phase 5). All free text is English (UK), the metadata master language."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Chapter(BaseModel):
    title_en: str = Field(description="Short chapter title in English")
    title_pt: str = Field(description="The same title in the style of the original Portuguese")
    first_block: str = Field(description="Block id where the chapter starts, e.g. b004")
    last_block: str
    summary: str = Field(description="1-3 plain, simple English sentences for a modern general reader")


class Term(BaseModel):
    term_pt: str = Field(description="Portuguese/Madeiran term as used (lemma, lower case unless proper)")
    block: str
    gloss_en: str = Field(description="Concise English gloss, e.g. 'fajã: flat coastal land formed by landslides'")
    category: Literal[
        "landform", "settlement", "agriculture", "water/irrigation", "administration", "church", "law/tenure",
        "measure/currency", "transport", "craft/industry", "food/drink", "folk culture", "flora/fauna name", "other",
    ]


class Person(BaseModel):
    as_written: str
    full_name: str = Field(description="Fullest form of the name given in the article")
    honorific: str | None = Field(description="D., Dr., Padre, Conde de ..., etc.")
    roles: list[str] = Field(description="Offices/occupations, English, e.g. 'governor of Madeira', 'bishop of Funchal'")
    birth: str | None = Field(description="EDTF date if stated, e.g. 1821, 1821-03-13, 18XX")
    death: str | None
    block: str
    note: str = Field(description="One self-contained footnote-style sentence: who they are and why they appear here")
    has_own_entry: bool = Field(description="True if this person is plausibly the subject of this very entry")


class Place(BaseModel):
    as_written: str
    name: str = Field(description="Canonical modern form of the place name, Portuguese")
    place_type: Literal[
        "island", "islet", "municipality", "parish", "town/city", "sítio/locality", "street/square", "building",
        "church/chapel", "fort", "quinta/estate", "peak/mountain", "plateau/serra", "valley/ravine", "river/stream",
        "levada", "spring/lake", "coast/bay/beach", "cape/point", "port/quay", "road/path", "region",
        "country", "foreign city/place", "other",
    ]
    parish: str | None = Field(description="Madeiran freguesia containing it, if known from the text")
    municipality: str | None
    island: Literal["Madeira", "Porto Santo", "Desertas", "Selvagens", "none"]
    geometry_hint: Literal["point", "line", "area"] = Field(description="line for levadas/rivers/roads; area for parishes, islands, serras")
    block: str
    note: str = Field(description="One self-contained sentence: why this place is mentioned in this entry")


class DateMention(BaseModel):
    as_written: str
    start: str = Field(description="EDTF: 1908, 1908-05, 1908-05-18, 15XX, 1566/1568, ~1450")
    end: str | None = Field(description="EDTF end for ranges")
    block: str
    event: str = Field(description="One self-contained footnote-style sentence: what happened then, per this entry")
    significance: Literal["major", "minor"]


class LinkPhrase(BaseModel):
    phrase: str = Field(description="Verbatim phrase in the Portuguese text")
    block: str
    target: str = Field(description="Headword the phrase most likely refers to in this encyclopedia (Portuguese)")
    explicit: bool = Field(description="True for explicit cross-references such as '(V. este nome)', 'V. Levadas'")


class Enrichment(BaseModel):
    id: str
    abstract: str = Field(description="1-2 plain English sentences summarising the entry")
    types: list[str] = Field(description="Taxonomy codes, most specific first")
    chapters: list[Chapter]
    terms: list[Term]
    persons: list[Person]
    places: list[Place]
    dates: list[DateMention]
    links: list[LinkPhrase]
