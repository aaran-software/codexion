from pydantic import BaseModel, create_model
from typing import List, Dict, Any, Optional, Type, get_args, get_origin

from pymysql import Date

FIELD_TYPE_MAP = {
    "textinput": str,
    "textarea": str,
    "password": str,
    "dropdown": str,
    "dropdownread": str,
    "switch": bool,
    "checkbox": bool,
    "calendar": Date,
    "date": Date,
    "file": str,
    "dropdownmultiple": List[str],
    "dropdownreadmultiple": List[str],
    "multicheckbox": List[str],
}

def build_dynamic_model_class(name: str, columns: List[Dict[str, Any]]) -> Type[BaseModel]:
    fields = {}

    for col in columns:
        field_name = col["key"]
        field_type = FIELD_TYPE_MAP.get(col["type"], str)

        # Optional[str] or Optional[List[str]] etc.
        fields[field_name] = (Optional[field_type], None)

    model = create_model(name, **fields)
    return model
