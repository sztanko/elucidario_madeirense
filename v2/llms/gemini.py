import os
import sys
import time

MODEL_NAME="gemini-2.0-flash-exp"

import google.generativeai as genai
MIN_TIME_SEC = 6.1
last_call = time.time()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def run_llm(config, text):
    global last_call
    retry_count = 5
    prompt = config["prompt"]
    schema = config["schema"]
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_schema": schema,
        "response_mime_type": "application/json",
    }
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config,
        system_instruction=prompt,
    )
    result = None
    while result is None and retry_count > 0:
        try:
            #chat_session = model.start_chat(
            #    history=[
            #    ]
            #    )
            t0=time.time()
            if t0 - last_call < MIN_TIME_SEC:
                time.sleep(MIN_TIME_SEC)
            last_call = time.time()
            result = model.generate_content(text, generation_config=generation_config)                        
            #if t1-t0 < MIN_TIME_SEC:
            #    time.sleep(0.1 + MIN_TIME_SEC - (t1-t0))
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write(f"Retrying in {MIN_TIME_SEC} seconds...\n")
            time.sleep(MIN_TIME_SEC)
            result = None
            retry_count -= 1
            if retry_count == 0:
                sys.stderr.write(f"Failed to generate content\n")
                raise

    return result