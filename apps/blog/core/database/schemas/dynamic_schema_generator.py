from pydantic import BaseModel, create_model
from typing import Optional, List, Dict, Any
from datetime import datetime


# 🔁 Map frontend field types to Python types
FIELD_TYPE_MAPPING = {
    "textinput": str,
    "textarea": str,
    "dropdown": str,
    "dropdownmultiple": List[str],
    "multicheckbox": List[str],
    "checkbox": bool,
    "switch": bool,
    "calendar": datetime,
    "date": datetime,
    "password": str,
    "file": str,
    "dropdownread": str,
    "dropdownreadmultiple": List[str],
}

# 🧠 Helper to get type from field type string
def get_python_type(field_type: str) -> Any:
    return FIELD_TYPE_MAPPING.get(field_type, str)


# 🔨 Generate dynamic Pydantic models
def generate_dynamic_schemas(model_name: str, field_definitions: List[Dict[str, Any]]):
    create_fields = {}
    update_fields = {}
    base_fields = {"id": (int, ...)}  # id included in read model

    for field in field_definitions:
        key = field["key"]
        field_type = field["type"]
        py_type = get_python_type(field_type)

        # All fields are optional in Update model
        update_fields[key] = (Optional[py_type], None)

        # Include only fields marked isForm for Create
        if field.get("isForm", True):
            create_fields[key] = (py_type, ...)

        # Include all fields for Read/ORM model
        base_fields[key] = (py_type, ...)

    CreateSchema = create_model(f"{model_name}Create", **create_fields)
    UpdateSchema = create_model(f"{model_name}Update", **update_fields)
    ReadSchema = create_model(f"{model_name}", __base__=BaseModel, **base_fields)
    ReadSchema.__config__.orm_mode = True

    return CreateSchema, UpdateSchema, ReadSchema
