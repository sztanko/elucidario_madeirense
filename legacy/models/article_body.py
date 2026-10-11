from typing import Dict, List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, constr




class ArticleBody(BaseModel):
    id: int = Field(..., description="Article ID extracted from HTML.")
    title: constr(strict=True) = Field(..., description="Corrected title in portuguese, not longer than original.")
    body: str = Field(
        ...,
        description="Convert the article text to Markdown. Important: Preserve every detail of the original Portuguese text. Do not summarize or omit any part. Replace HTML tags with appropriate Markdown syntax. Pay special attention to tables, lists, and quotes. Use '##' for headers only.",
    )

if __name__ == "__main__":
    import json

    schema = json.dumps(Article.model_json_schema(), indent=2, ensure_ascii=False)
    print(schema)
