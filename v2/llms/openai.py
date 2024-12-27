import os
import sys
import time
from openai import OpenAI

MODEL_NAME = "gpt-4o"
MIN_TIME_SEC = 6

# Configure OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_llm(config, text):
    """
    Function to interact with OpenAI's GPT-4o-mini model using a defined schema.

    Args:
        config (dict): Configuration dictionary containing 'prompt' and 'schema'.
        text (str): The input text for the model.

    Returns:
        SchemaModel: Parsed response based on the defined schema.
    """
    retry_count = 5
    prompt = config["prompt"]
    schema = config["schema"]  # This should reference a Pydantic model

    result = None
    while result is None and retry_count > 0:
        try:
            t0 = time.time()
            completion = client.beta.chat.completions.parse(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                response_format=schema,
            )
            t1 = time.time()

            if t1 - t0 < MIN_TIME_SEC:
                time.sleep(0.1 + MIN_TIME_SEC - (t1 - t0))

            # Extract the parsed response
            result = completion.choices[0].message.parsed
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write(f"Retrying in {MIN_TIME_SEC} seconds...\n")
            time.sleep(MIN_TIME_SEC)
            result = None
            retry_count -= 1
            if retry_count == 0:
                sys.stderr.write("Failed to generate content\n")
                raise

    return result.dict()
