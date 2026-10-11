from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import typer
import os
import black
from io import StringIO
from typing import Optional
from jinja2 import Template
from utils.llm import call_llm, LlmOpts, LLM
from utils.logging import get_logger
from utils.xml import dict_to_xml_str

log = get_logger(__name__)

app = typer.Typer(pretty_exceptions_enable=False)


def get_files_contents(path: str, exclude_files: List[str]) -> Dict[str, str]:
    """Get the content of all files in a directory and it's subdirectories"""
    out = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".py"):
                continue
            if file in exclude_files:
                log.info(f"Skipping file: {file}")
                continue
            full_path = os.path.join(root, file)
            if "__pycache__" in full_path:
                continue
            log.info(f"Reading file: {full_path}")
            with open(full_path, "r") as f:
                out["file " + full_path] = f.read()
    return out


""" declare a pydantic model containing two fields: graph definition and schema models """

def format_python_code(code: str) -> str:
    """Format the python code using black"""
    try:
        # Create a StringIO object to capture the formatted code
        return black.format_str(code, mode=black.FileMode())
        
    except Exception as e:
        log.error(f"Error formatting code: {e}")
        return code
    

class Output(BaseModel):
    imports_code: str = Field(..., description="Python import instructions needed for the code to run")
    steps_code: str = Field(
        ...,
        description="List of Step class instances, python code. This list shoudl be assigned to a variable named 'workflow'",
    )
    processors_code: str = Field(..., description="List of functions that process the input or output of the LLM")
    output_schemas_code: str = Field(
        ..., description="List of Pydantic schema classes, that are used in the steps as output_schema"
    )


PROMPT = """
    I am processing a portuguese encyclopedia writtien in 1930-ies.     
    I need to clean it up, extract structural information, classify the articles and translate them.
    For this, I have created a framework where I can define tasks as steps and process them one by one in a DAG-like manner.
    Each step can involve calling an LLM, then processing it's output.
    Based on the code of the framework provided and a yaml file that losely defines the steps, create a precise definition of the steps (a list of Step class instances).
    Also write down the schemas for each output_schema field of the Step class instances, and processors - functions that process input or output.
    """

out_template = """
{{ imports_code }}

# Output schemas
{{ output_schemas_code }}

# Processors
{{ processors_code }}

# Steps definition
{{ steps_code }}
"""

def generate_code(yaml_file: str, output_file_name: str) -> Output:
    """Generate the code for the framework based on the yaml file"""
    # get the contents of the yaml file as string
    log.info(f"Reading the yaml file: {yaml_file}")
    with open(yaml_file, "r") as f:
        yaml_content = f.read()
    # get file contents of the current directory
    current_dir = "v3" # os.path.dirname(os.path.realpath(__file__))
    files_contents = get_files_contents(
        current_dir, exclude_files=["llm_test.py", "gen_graph.py", "workflow.py", "logging.py", "xml.py"]
    )
    log.info(f"Read {len(files_contents)} files")
    code = dict_to_xml_str(files_contents)
    # log.info(files_contents)
    # log.info(f"Code: {code}")
    # return
    # call the LLM to generate the code
    # log.info(files_contents)
    llm_type = LLM.OPEN_AI_POWER
    opts = LlmOpts(llm=llm_type)
    data = {"yaml": yaml_content, "code": files_contents}
    log.info(f"Calling the LLM {llm_type}")
    response = call_llm(PROMPT, opts, data, Output)
    # write the generated code to a file
    with open(output_file_name, "w") as f:
        template = Template(out_template)
        rendered = template.render(**response.model_dump())
        # log.info(rendered)
        log.info(f"Formatting the generated code")
        formatted_code = format_python_code(rendered)
        log.info(f"Writing the generated code to: {output_file_name}")
        f.write(formatted_code)
    # Now, import the generated code, run it and take the workflow variable
    log.info(f"Importing the generated code")
    import_path = os.path.splitext(output_file_name)[0].replace("/", ".")
    import_path = import_path.replace("\\", ".")
    import_path = import_path.replace(".py", "")
    log.info(f"Importing the generated code from: {import_path}")
    import importlib
    import sys
    import types
    module = importlib.import_module(import_path)
    workflow = getattr(module, "workflow", None)
    if workflow is None:
        raise ValueError(f"Workflow variable not found in the generated code")
    mermaid = generate_mermaid_graph(workflow)
    # log.info(f"Generated mermaid graph:\n {mermaid}")
    return mermaid


@app.command()
def r(yaml_file: str, output_file_name: str):
    if not output_file_name.endswith(".py"):
        raise ValueError("Output file name must end with .py")
    generate_code(yaml_file, output_file_name)


if __name__ == "__main__":
    app()
