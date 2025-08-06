from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()


def get_nested(data, path):
    keys = path.split(".")
    for key in keys:
        data = data.get(key, {})
    return data


from typing import List

FIELD_TYPE_MAP = {
    "textinput": "str",
    "textarea": "str",
    "password": "str",
    "dropdown": "str",
    "dropdownread": "str",
    "switch": "bool",
    "checkbox": "bool",
    "calendar": "str",  # You can change this to "datetime" if needed
    "date": "str",      # Or use "date"
    "file": "str",
    "dropdownmultiple": "List[str]",
    "dropdownreadmultiple": "List[str]",
    "multicheckbox": "List[str]",
}

def create_model_and_schema(name: str, fields: list):
    model_path = Path(__file__).resolve().parent.parent / "models"
    schema_path = Path(__file__).resolve().parent.parent / "database" / "schemas"

    model_path.mkdir(parents=True, exist_ok=True)
    schema_path.mkdir(parents=True, exist_ok=True)

    model_file = model_path / f"{name.lower()}.py"
    schema_file = schema_path / f"{name.lower()}_schema.py"

    if not model_file.exists():
        with model_file.open("w") as f:
            f.write("from sqlalchemy import Column, String\n")
            f.write("from cortex.DTO.dal import Base\n\n")
            f.write(f"class {name.capitalize()}(Base):\n")
            f.write(f"    __tablename__ = '{name.lower()}'\n")
            for field in fields:
                key = field["key"]
                f.write(f"    {key} = Column(String)\n")

    if not schema_file.exists():
        with schema_file.open("w") as f:
            f.write("from pydantic import BaseModel\n")
            f.write("from typing import Optional\n")
            f.write("from datetime import datetime\n\n")

            # Create schema
            f.write(f"class {name.capitalize()}Create(BaseModel):\n")
            for field in fields:
                key = field["key"]
                if key == "id":
                    continue
                f.write(f"    {key}: str\n")  # You can infer type from `field["type"]` if needed
            f.write("\n")

            # Update schema (same fields as Create for now)
            f.write(f"class {name.capitalize()}Update(BaseModel):\n")
            for field in fields:
                key = field["key"]
                if key == "id":
                    continue
                f.write(f"    {key}: str\n")
            f.write("\n")

            # Read schema
            f.write(f"class {name.capitalize()}(BaseModel):\n")
            for field in fields:
                key = field["key"]
                f.write(f"    {key}: str\n")
            f.write("    created_at: Optional[datetime] = None\n\n")
            f.write("    class Config:\n")
            f.write("        orm_mode = True\n")


@router.get("/dynamic/{name}")
def dynamic_init(name: str, json_path: str, field_path: str):
    """
    Example call: /dynamic/blog?json_path=data/blog.json&field_path=blog.blogs.details.fields
    """
    json_file = Path(__file__).resolve().parent.parent / json_path

    if not json_file.exists():
        return {"error": "JSON config file not found."}

    with open(json_file) as f:
        config = json.load(f)

    fields = get_nested(config, field_path)

    if not isinstance(fields, list) or not all("key" in field for field in fields):
        return {"error": "Invalid field path or structure."}

    create_model_and_schema(name, fields)

    return {"message": f"Model and schema for '{name}' created from '{field_path}'."}
