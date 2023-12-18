from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field, constr


class Translation(BaseModel):
    id: int = Field(..., description="Article ID")
    title: constr(strict=True) = Field(..., description="Translation of title")
    preceeding_text: Optional[str] = Field(
        None,
        description="Text preceding the article chunk to translate. This is only to aid you in translating the body. DO NOT INCLUDE IN THE OUTPUT.",
    )
    body: str = Field(
        ...,
        description="Precise Translation of body. Keep the markdown formatting precisely. Do not leave out any details. Preserve layout.",
    )
    locations: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Translated locations. Keep in mind these are descriptions of geographicals locations. Populate only if input contains this key.",
    )
    people: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Keys are people mentioned in the article, values are portuguese descriptions of the context in which they are mentioned. Translate both keys and values. Populate only if input contains this key.",
    )
    years: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Keys are years mentioned in the article, values are translations of descriptions of the context in which that year was mentioned. Populate only if input contains this key.",
    )


if __name__ == "__main__":
    import json

    schema = json.dumps(Translation.model_json_schema(), indent=2, ensure_ascii=False)
    print(schema)
