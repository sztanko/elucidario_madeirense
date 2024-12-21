import os
import sys

MODEL_NAME="gemini-2.0-flash-exp"

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def run_llm(config, text):
    prompt = config["prompt"]
    schema = config["schema"]
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": schema,
        "response_mime_type": "application/json",
    }
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config,
        system_instruction=prompt,
    )
    chat_session = model.start_chat(
        history=[
        ]
        )
    result = model.generate_content(text, generation_config=generation_config)
    return result