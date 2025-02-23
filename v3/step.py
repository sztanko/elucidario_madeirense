from typing import List, Callable, Dict
from dataclasses import dataclass
from pydantic import BaseModel, Field
from google.ai.generativelanguage_v1beta.types.content import Schema

@dataclass
class Step:
    name: str
    description: str
    input_tags: List[str]
    prompt: str
    output_tags: List[str]
    additional_context: Dict[str, str]
    postprocessing: callable
    output_schema: Schema


