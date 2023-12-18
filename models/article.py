from typing import Dict, List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, constr


class Article(BaseModel):
    id: int = Field(..., description="Article ID extracted from HTML.")
    title: constr(strict=True) = Field(..., description="Corrected title in portuguese, not longer than original.")
    body: str = Field(
        ...,
        description="Convert the article text to Markdown accurately. IMPORTANT: Preserve every detail of the original Portuguese text. Do not summarize or omit any part. Format ALL quotations as blockquotes (>) in Markdown. Everything that looks like a table should be presented as markdown table. Convert ALL enumerations or lists to Markdown formatted lists. If any text seems suitable for highlighting but isn't explicitly marked, italicize it for emphasis. Use only '##' for headers. Split the paragraphs if longer then 400 words.",
    )
    categories: List[
        Literal[
            "Geografia",
            "História",
            "Biologia",
            "Cultura",
            "Arquitetura",
            "Política",
            "Economia",
            "Sociedade",
            "Religião",
            "Educação",
            "Saúde",
            "Arte",
            "Ciência",
            "Desporto",
            "Transporte",
        ]
    ] = Field(
        ...,
        description="Come up with max 3 categories where this article belongs to based on it's content. There ALWAYS must be at least one category. Strictly only these categories are allowed:"
        "Geografia - geographical features like mountains, rivers, and islands. "
        "História -  historical events, personages, and historical context. "
        "Biologia - flora, fauna, and natural species descriptions. "
        "Cultura - local traditions, folklore, and cultural practices. "
        "Arquitetura - buildings, monuments, and architectural styles. "
        "Política - political figures, governmental structures, and political history. "
        "Economia - industries, commerce, and economic changes. "
        "Sociedade - societal norms, demographics, and community structures. "
        "Religião - religious practices, churches, and religious figures. "
        "Educação - schools, educational reforms, and notable educators. "
        "Saúde - hospitals, health crises, and medical practices. "
        "Arte - local artists, artistic movements, and cultural artifacts. "
        "Ciência - scientific discoveries, research, and scientific figures. "
        "Desporto - sports, athletic events, and notable athletes. "
        "Transporte - modes of transportation, infrastructure, and related developments.",
    )
    references: Optional[List[str]] = Field(
        default_factory=list,
        description="List of references to other articles mentioned in the body or title of article. References often are prepended with `v.` or `Vid.`. Sometimes the title is containing a reference, in this case the new title needs to be there without the reference, and the reference itself added to `references`. If body is empty in this case, just duplicate the reference there.",
    )
    locations: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Extract information about ALL geographical locations mentioned in the article. Keys are location, values are concise factual information in portuguese about mentions of this location in the article. In the value, don't mention the location name itself",
    )
    freguesias: Optional[List[str]] = Field(default_factory=list, description="List of freguesias mentioned, if any.")
    people: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Extract information about ALL persons mentioned in the article. Keys are are people, values are concise factual information in portuguese about mentions of this person in the article. In the value, don't mention the person, just tell who was that.",
    )
    years: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Extract information about ALL years mentioned in the article. Keys are years (integers), values are concise factual information in portuguese about mentions of this year in the article. In the value, directly state the event WITHOUT mentioning the year. DO NOT start the value with 'ano em que', 'ano de' or similar.",
    )


if __name__ == "__main__":
    import json

    schema = json.dumps(Article.model_json_schema(), indent=2, ensure_ascii=False)
    print(schema)
