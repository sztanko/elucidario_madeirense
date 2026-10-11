from typing import List, Callable, Dict, Optional, Union, Tuple
from logging import log
from dataclasses import dataclass
from jinja2 import Template
from pydantic import BaseModel, Field
from .utils.llm import call_llm, LlmOpts


@dataclass
class Step:
    name: str = Field(..., description="Name of the step")
    description: str = Field(..., description="Description of the step")
    depends_on: List[str] = Field(..., description="List of steps that this step depends on. Must exist.")
    unique_keys: List[str] = Field(
        ..., description="List of keys that are unique for this step. This is used to group the data by these keys."
    )

    precondition: Callable = Field(
        ..., description="Function that checks if the step can be executed. It should return True or False."
    )
    prompt: Optional[str] = Field(
        None,
        description="Prompt Jinja2 template for the LLM. If not provided, the step will not call the LLM. When converting from yaml, make it a jinja template, fix the syntax, if needed. Typically this is a multi-line string",
    )
    llm_opts: Optional[LlmOpts] = Field(
        None, description="Options for the LLM. If not provided, the step will not call the LLM."
    )
    flatten_output: bool = Field(
        False,
        description="If True, the output will be flattened, that is, each element of an array will be added as a separate output.",
    )
    # additional_context: Dict[str, str] = Field(..., description="Additional context for the LLM. This is used to provide additional information to the LLM.")
    preprocessor: Callable = Field(
        ..., description="Gets all the inputs from previous steps (dependancies) and transforms it into another structure"
    )
    postprocessor: Callable = Field(
        ..., description="Gets the output from the LLM and transforms it into another structure"
    )
    output_schema: BaseModel = Field(
        ..., description="Pydantic schema for the output of the step. This is used to validate the output of the step."
    )


def get_order_of_execution(steps: List[Step]) -> List[Step]:
    # This function should return a list of steps in the order they should be
    # This all is based on depends_on field in the Step class
    added_steps = set()
    order = []
    steps_added = True
    remaining_steps = set(step.name for step in steps)
    while steps_added:
        steps_added = False
        for step_name in remaining_steps:
            step = next(step for step in steps if step.name == step_name)
            # if all dependencies are already added, add the step
            if all(dep in added_steps for dep in step.depends_on):
                order.append(step)
                added_steps.add(step.name)
                steps_added = True
                remaining_steps.remove(step.name)
    if remaining_steps:
        raise ValueError(f"Could not find order of execution for steps: {remaining_steps}")
    return order


def group_data_by_unique_keys(data: List[Dict[str, any]], unique_keys: List[str]) -> Dict[Tuple, List[Dict[str, any]]]:
    grouped_data = {}
    for item in data:
        key = tuple(item[key] for key in unique_keys)
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item)
    return grouped_data


def merge_data(data: Dict[str, Dict[Tuple, List[Dict[str, any]]]]) -> Dict[Tuple, Dict[str, List[Dict[str, any]]]]:
    merged_data = {}
    for source_name, source_data in data.items():
        for row, items in source_data.items():
            if row not in merged_data:
                merged_data[row] = {}
            merged_data[row][source_name] = items
    return merged_data


class Graph:
    steps: List[Step]

    def __init__(self, steps: List[Step]):
        self.steps = get_order_of_execution(steps)
        self.queues = {}

    def add_to_queue(self, queue_name, obj):
        if queue_name not in self.queues:
            self.queues[queue_name] = []
        self.queues[queue_name].append(obj)

    def process(self, data: List):
        for step in self.steps:
            if not step.depends_on:
                input_data = data
            else:
                data_from_all_dependencies = {
                    dep: group_data_by_unique_keys(self.queues[dep], step.unique_keys) for dep in step.depends_on
                }
                input_data = merge_data(data_from_all_dependencies)
            output_data = []
            for d in input_data.values():
                output_data.add(self.process_step(step, d))

            self.add_to_queue(step.name, data)

    def process_step(self, step: Step, input_data: Dict[str, any]) -> Dict[str, any]:
        if not step.precondition(input_data):
            raise ValueError(f"Precondition failed for step {step.name}")
        if step.preprocessor:
            prepared_data = step.preprocessor(input_data)
        else:
            prepared_data = input_data
        if prompt:
            # Render the jinja template with the prepared data
            template = Template(step.prompt)
            rendered_prompt = template.render(**prepared_data)
            output = call_llm(rendered_prompt, step.llm_opts, prepared_data, step.output_schema)
        else:
            output = prepared_data
        if step.postprocessor:
            processed_data = step.postprocessing(output)
        else:
            processed_data = output
        # if processed data is an array and flatten is True, flatten the array, and add 'index' as a key
        output_data = []
        if step.flatten_output and isinstance(processed_data, list):
            # Make multiple outputs out of a single one.
            for index, item in enumerate(processed_data):
                item["index"] = index
                output_data.append(item)
        else:
            output_data.append(processed_data)
        return output_data

def generate_mermaid_graph(workflow):
    lines = ["graph TD"]
    step_names = {step.name for step in workflow}
    for step in workflow:
        for dep in step.depends_on:
            if dep in step_names:
                lines.append(f"    {dep} --> {step.name}")
        if not step.depends_on:
            lines.append(f"    {step.name}")
    return "\n".join(lines)
