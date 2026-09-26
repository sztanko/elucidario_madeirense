from typing import Optional
from pydantic import BaseModel
from utils.llm import call_llm, LlmOpts, LLM


def test_all_llms():
    # Schema
    class PersonInfo(BaseModel):
        name: str
        age: int
        predicted_nationality: str
        gender: str

    # Prompt template
    prompt = "Extract name and age from the following XML. Make up missing fields based on your best guess"

    # Data
    data = {"text": "This guy is called Dimi, he has brown hair and is about 40 years old"}

    for model in LLM:
        print(model)
        opts = LlmOpts(llm=model)

        # Call
        response = call_llm(prompt, opts, data, PersonInfo)
        print(response)

def test_long_output_google():
    # Schema
    class PersonInfo(BaseModel):
        name: str
        age: int
        predicted_nationality: str
        gender: str
    # Prompt template
    prompt = "Extract name and age from the following XML. Make up missing fields based on your best guess"
    
    data = {"text": "This guy is called Dimi, she has brown hair and is about 40 years old"}
    for i in range(0,1000):
        data[f"field_{i}"] = f"Value {i}"
    opts = LlmOpts(llm=LLM.GOOGLE_POWER)
    response = call_llm(prompt, opts, data, PersonInfo)
    print(response)

# test_long_output_google()
test_all_llms()