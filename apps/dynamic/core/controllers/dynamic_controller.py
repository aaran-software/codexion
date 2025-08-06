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
    "calendar": "date",  # You can change this to "datetime" if needed
    "date": "date",  # Or use "date"
    "file": "str",
    "dropdownmultiple": "List[str]",
    "dropdownreadmultiple": "List[str]",
    "multicheckbox": "List[str]",
}
SQLA_TYPE_MAP = {
    "str": "String",
    "bool": "Boolean",
    "datetime": "DateTime",
    "List[str]": "JSON",
}

def create_model_and_schema(name: str, fields: list):
    model_path = Path(__file__).resolve().parent.parent / "models"
    schema_path = Path(__file__).resolve().parent.parent / "database" / "schemas"
    controller_path = Path(__file__).resolve().parent.parent / "controllers"

    model_path.mkdir(parents=True, exist_ok=True)
    schema_path.mkdir(parents=True, exist_ok=True)

    model_file = model_path / f"{name.lower()}.py"
    schema_file = schema_path / f"{name.lower()}_schema.py"
    controller_file = controller_path / f"{name.capitalize()}Controller.py"

    model_file.parent.mkdir(parents=True, exist_ok=True)

    if not model_file.exists():
        with model_file.open("w") as f:
            # Write imports
            f.write("from sqlalchemy.orm import Mapped, mapped_column\n")
            f.write("from sqlalchemy import String, Boolean, DateTime, JSON, Date\n")
            f.write("from cortex.DTO.dal import Base\n\n")
            f.write("from typing import List\n")
            f.write("from datetime import datetime, date\n\n")

            # Write class
            f.write(f"class {name.capitalize()}(Base):\n")
            f.write(f"    __tablename__ = '{name.lower()}'\n\n")

            for field in fields:
                key = field["key"]
                field_type = FIELD_TYPE_MAP.get(field["type"], "str")

                # ID field
                if key == "id":
                    f.write(f"    {key}: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)\n")
                elif field_type == "str":
                    f.write(f"    {key}: Mapped[str] = mapped_column(String(255))\n")
                elif field_type == "bool":
                    f.write(f"    {key}: Mapped[bool] = mapped_column(Boolean)\n")
                elif field_type == "datetime":
                    f.write(f"    {key}: Mapped[datetime] = mapped_column(DateTime)\n")
                elif field_type == "date":
                    f.write(f"    {key}: Mapped[date] = mapped_column(Date)\n")
                elif field_type.startswith("List"):
                    f.write(f"    {key}: Mapped[{field_type}] = mapped_column(JSON)\n")
                else:
                    f.write(f"    {key}: Mapped[{field_type}] = mapped_column()\n")

    if not schema_file.exists():
        needs_list = any("List" in FIELD_TYPE_MAP.get(field["type"], "str") for field in fields)
        with schema_file.open("w") as f:
            f.write("from pydantic import BaseModel\n")
            if needs_list:
                f.write("from typing import Optional, List\n")
            else:
                f.write("from typing import Optional\n")
            f.write("from datetime import datetime\n")
            f.write("from pymysql import Date\n\n")

            # Create schema
            f.write(f"class {name.capitalize()}Create(BaseModel):\n")
            for field in fields:
                key = field["key"]
                if key == "id":
                    continue
                field_type = FIELD_TYPE_MAP.get(field["type"], "str")
                f.write(f"    {key}: {field_type}\n")
            f.write("\n")

            # Update schema
            f.write(f"class {name.capitalize()}Update(BaseModel):\n")
            for field in fields:
                key = field["key"]
                if key == "id":
                    continue
                field_type = FIELD_TYPE_MAP.get(field["type"], "str")
                f.write(f"    {key}: Optional[{field_type}] = None\n")
            f.write("\n")

            # Read schema
            f.write(f"class {name.capitalize()}(BaseModel):\n")
            for field in fields:
                key = field["key"]
                field_type = FIELD_TYPE_MAP.get(field["type"], "str")
                f.write(f"    {key}: {field_type}\n")
            f.write("    created_at: Optional[datetime] = None\n\n")
            f.write("    class Config:\n")
            f.write("        from_attributes = True\n")
            # f.write("        orm_mode = True\n")

    # CONTROLLER
    if not controller_file.exists():
        with controller_file.open("w") as f:
            f.write("from fastapi import APIRouter, Depends, HTTPException, Request\n")
            f.write("from sqlalchemy.orm import Session\n")
            f.write("from typing import List\n\n")
            f.write(f"from apps.dynamic.core.database.schemas import {name.lower()}_schema\n")
            f.write(f"from apps.dynamic.core.models.{name.lower()} import {name.capitalize()}\n")
            f.write("from cortex.DTO.dal import get_db\n\n")
            f.write(f"router = APIRouter(prefix='/{name.lower()}', tags=['{name.lower()}'])\n\n")

            # CREATE
            f.write(f"@router.post('/', response_model=List[{name.lower()}_schema.{name.capitalize()}])\n")
            f.write("async def create_items(request: Request, db: Session = Depends(get_db)):\n")
            f.write("    data = await request.json()\n")
            f.write("    if isinstance(data, dict):\n")
            f.write("        data = [data]\n")
            f.write(f"    items = [{name.lower()}_schema.{name.capitalize()}Create(**item) for item in data]\n")
            f.write(f"    db_items = [{name.capitalize()}(**item.dict()) for item in items]\n")
            f.write("    db.add_all(db_items)\n")
            f.write("    db.commit()\n")
            f.write("    for item in db_items:\n")
            f.write("        db.refresh(item)\n")
            f.write("    return db_items\n\n")

            # READ ONE
            f.write(f"@router.get('/{{item_id}}', response_model={name.lower()}_schema.{name.capitalize()})\n")
            f.write("def read_item(item_id: str, db: Session = Depends(get_db)):\n")
            f.write(f"    item = db.query({name.capitalize()}).filter({name.capitalize()}.id == item_id).first()\n")
            f.write("    if not item:\n")
            f.write("        raise HTTPException(status_code=404, detail='Item not found')\n")
            f.write("    return item\n\n")

            # READ ALL
            f.write(f"@router.get('/', response_model=List[{name.lower()}_schema.{name.capitalize()}])\n")
            f.write("def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):\n")
            f.write(f"    return db.query({name.capitalize()}).offset(skip).limit(limit).all()\n\n")

            # UPDATE
            f.write(f"@router.put('/{{item_id}}', response_model={name.lower()}_schema.{name.capitalize()})\n")
            f.write(
                f"def update_item(item_id: str, data: {name.lower()}_schema.{name.capitalize()}Update, db: Session = Depends(get_db)):\n")
            f.write(f"    db_item = db.query({name.capitalize()}).filter({name.capitalize()}.id == item_id).first()\n")
            f.write("    if not db_item:\n")
            f.write("        raise HTTPException(status_code=404, detail='Item not found')\n")
            f.write("    for key, value in data.dict(exclude_unset=True).items():\n")
            f.write("        setattr(db_item, key, value)\n")
            f.write("    db.commit()\n")
            f.write("    db.refresh(db_item)\n")
            f.write("    return db_item\n\n")

            # DELETE
            f.write(f"@router.delete('/{{item_id}}', response_model={name.lower()}_schema.{name.capitalize()})\n")
            f.write("def delete_item(item_id: str, db: Session = Depends(get_db)):\n")
            f.write(f"    db_item = db.query({name.capitalize()}).filter({name.capitalize()}.id == item_id).first()\n")
            f.write("    if not db_item:\n")
            f.write("        raise HTTPException(status_code=404, detail='Item not found')\n")
            f.write("    db.delete(db_item)\n")
            f.write("    db.commit()\n")
            f.write("    return db_item\n")


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
