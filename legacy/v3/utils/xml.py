from typing import Any, Union
import xml.sax.saxutils as saxutils

def dict_to_xml_str(data: Any) -> str:
    """
    Recursively converts a dictionary or list into an XML string.

    - Dict keys become tags.
    - List items are wrapped in <item> tags.
    - Text content is properly escaped.
    """
    def escape(value: Union[str, int, float, bool, None]) -> str:
        if value is None:
            return ""
        return saxutils.escape(str(value))

    def recurse(value: Any) -> str:
        if isinstance(value, dict):
            parts = []
            for key, val in value.items():
                if not isinstance(key, str): # or not key.isidentifier():
                    continue
                parts.append(f"<{key}>{recurse(val)}</{key}>")
            return "\n".join(parts)
        elif isinstance(value, list):
            return "\n".join(f"<item>{recurse(item)}</item>" for item in value)
        else:
            return escape(value)

    return recurse(data)