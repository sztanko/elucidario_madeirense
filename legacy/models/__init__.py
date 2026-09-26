from pydantic import BaseModel, create_model
from typing import Type, List

def create_list_model(model: Type[BaseModel]) -> Type[BaseModel]:
    """
    Factory function to create a Pydantic model with a single field 'a'
    that is a list of instances of the provided model class.

    :param model: The Pydantic model class to be used as the list item type.
    :return: A new Pydantic model class.
    """
    return create_model(
        'ListModel', 
        a=(List[model], ...)
    )

# Example usage
# class ItemModel(BaseModel):
#     name: str
#     value: int

# Create a new model with a list of ItemModel
# ListModel = create_list_model(ItemModel)

# Example of using the new ListModel
# example = ListModel(a=[ItemModel(name="item1", value=1), ItemModel(name="item2", value=2)])
# print(example.json())