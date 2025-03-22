from typing import List, Callable, Dict, Optional, Union
from logging import log
from dataclasses import dataclass
from pydantic import BaseModel, Field
from .utils.llm import call_llm


@dataclass
class Step:
    name: str
    description: str
    depends_on: List[str]
    unique_keys: List[str]
    precondition: Callable
    prompt: Optional[Union[str, Callable]]
    llm_opts: Optional[Dict[str, any]]  # typically what llm to use
    flatten_output: bool
    additional_context: Dict[str, str]
    preprocessor: Callable  # Get's all the inputs from previous steps and transforms it into another structure
    postprocessor: Callable  # Get's the output from the LLM and transforms it into another structure
    output_schema: BaseModel  # Pydantic schema for the output of the step


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
            # TODO: implement llm call, together with the schema validation
            output = call_llm(step.prompt, step.llm_opts, prepared_data, step.output_schema)
        else:
            output = prepared_data
        if step.postprocessor:
            processed_data = step.postprocessing(output)
        else:
            processed_data = output
        # if prepared data is an array and flatten is True, flatten the array, and add 'index' as a key
        if step.flatten_output and isinstance(prepared_data, list):
            output_data = []
            for index, item in enumerate(prepared_data):
                item["index"] = index
                output_data.append(item)
        return output_data
