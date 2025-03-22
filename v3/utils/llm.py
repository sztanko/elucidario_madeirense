from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
from pydantic import BaseModel

class LLM(Enum):
    OPEN_AI_MINI = auto()
    OPEN_AI_POWER = auto()
    GOOGLE_MINI = auto()
    GOOGLE_POWER = auto()
    CLAUDE_MINI = auto()
    CLAUDE_POWER = auto()

@dataclass
class LlmOpts:
    llm: LLM
    temperature: Optional[float]
    max_tokens: Optional[int]
    top_p: Optional[float]



def call_llm(prompt: str, options: LlmOpts,  data: Any, schema: BaseModel) -> Any:
    pass