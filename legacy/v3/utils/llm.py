from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Any, Type
from pydantic import BaseModel
import instructor
from jinja2 import Template
import xml.sax.saxutils as saxutils
# from instructor.clients import OpenAIClient, AnthropicClient, GoogleClient
from instructor.mode import Mode
from openai import OpenAI
from anthropic import Anthropic
# from google.generativeai import GenerativeModel
from google import genai
from .xml import dict_to_xml_str
from .logging import get_logger

log = get_logger(__name__)

MAX_TOKENS = 16384

# Define enum
class LLM(Enum):
    OPEN_AI_MINI = auto()
    OPEN_AI_POWER = auto()
    GOOGLE_MINI = auto()
    GOOGLE_POWER = auto()
    CLAUDE_MINI = auto()
    CLAUDE_POWER = auto()

MAX_TOKENS_MAP = {
    LLM.OPEN_AI_MINI: 2*16384,
    LLM.OPEN_AI_POWER: 2*16384,
    LLM.GOOGLE_MINI: 128*1024,
    LLM.GOOGLE_POWER: 128*1024,
    LLM.CLAUDE_MINI: 4096,
    LLM.CLAUDE_POWER: 4096,
}

# Options for LLM
@dataclass
class LlmOpts:
    llm: LLM
    temperature: Optional[float] = 0.0

# Client init (reuse clients for efficiency)
openai_client = instructor.from_openai(OpenAI(), mode=Mode.TOOLS_STRICT)
claude_client = instructor.from_anthropic(Anthropic())
gemini_client = instructor.from_genai(genai.Client())

# Model map
LLM_MODEL_MAP = {
    LLM.OPEN_AI_MINI: ("gpt-4.1-mini", openai_client),
    LLM.OPEN_AI_POWER: ("gpt-4.1", openai_client),
    LLM.CLAUDE_MINI: ("claude-3-haiku-20240307", claude_client),
    LLM.CLAUDE_POWER: ("claude-3-opus-20240229", claude_client),
    LLM.GOOGLE_MINI: ("gemini-2.5-flash-preview-04-17", gemini_client),
    LLM.GOOGLE_POWER: ("gemini-2.5-pro-preview-05-06", gemini_client),
}

# Main call
def call_llm(prompt: str, options: LlmOpts, data: Any, schema: Type[BaseModel]) -> BaseModel:
    model_name, client = LLM_MODEL_MAP[options.llm]
    template = Template(prompt)
    rendered_prompt = template.render(**data)
    xml_data = dict_to_xml_str(data)
    # xml_data should be string
    assert isinstance(xml_data, str)
    # log.info(f"Prompt: {rendered_prompt}")
    # log.info(f"XML: {xml_data}")
    max_tokens = MAX_TOKENS_MAP[options.llm]
    
    if options.llm in [LLM.OPEN_AI_MINI, LLM.OPEN_AI_POWER]:
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns JSON." + rendered_prompt},
                {"role": "user", "content": xml_data}
            ],
            temperature=options.temperature,
            max_tokens=max_tokens,
            response_model=schema
        )
    if options.llm in [LLM.CLAUDE_MINI, LLM.CLAUDE_POWER]:
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns JSON." + rendered_prompt},
                {"role": "user", "content": xml_data}
            ],
            response_model=schema,
            max_tokens=max_tokens,
            temperature=options.temperature
        )
    if options.llm in [LLM.GOOGLE_MINI, LLM.GOOGLE_POWER]:
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": rendered_prompt},
                # {"role": "system", "content": xml_data},
                {"role": "user", "content": f"{xml_data}"}
            ],
            response_model=schema,
        )
    raise ValueError("Unsupported client or model")
