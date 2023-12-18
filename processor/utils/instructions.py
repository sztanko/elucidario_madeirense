from typing import Type
import json
import logging

from models import create_list_model
from pydantic import BaseModel

def load_instructions(template_file, **variables):
    """
    Given a template file, return the template with the given kwargs
    Example content of template file: "Hello {name}"
    """
    logging.info(f"Loading instructions from {template_file}")
    with open(template_file, "r") as f:
        template = f.read()
        # logging.info(variables)
        formatted_template = template.format(**variables)
        #logging.info(f"Instructions from {template_file}: {formatted_template}")
        logging.info(f"Loaded {len(formatted_template)} characters from {template_file}")
        return formatted_template

def make_output_schema_instructions(model: Type[BaseModel], as_list: bool = False):
    """
    Given a Pydantic model, return the instructions for the model
    """
    if as_list:
        model = create_list_model(model)
    schema = json.dumps(model.model_json_schema(), indent=2, ensure_ascii=False)
    
    # output strict output instructions for LLM 
    return f"""
    Output format: return a valid json STRICTLY OBEYING the following JSON Schema:
    ```
    {schema}
    ```
    Don't write any text before of after the json, only just the json.
    
    """
    