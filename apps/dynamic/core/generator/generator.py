from pathlib import Path

def generate_schema_file(name: str, fields: dict):
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / f"{name}_schema.py"
    if schema_path.exists():
        return

    lines = ["from pydantic import BaseModel\n\n"]
    lines.append(f"class {name.capitalize()}Create(BaseModel):\n")
    for field_name, field_type in fields.items():
        lines.append(f"    {field_name}: {field_type}\n")

    schema_path.write_text("".join(lines))


def generate_model_file(name: str, fields: dict):
    model_path = Path(__file__).resolve().parent.parent / "models" / f"{name}.py"
    if model_path.exists():
        return

    lines = [
        "from sqlalchemy import Column, Integer, String\n",
        "from cortex.database import Base\n\n",
        f"class {name.capitalize()}(Base):\n",
        f"    __tablename__ = '{name}'\n",
        "    id = Column(Integer, primary_key=True, index=True)\n"
    ]
    for field_name, field_type in fields.items():
        # crude mapping for example
        sql_type = "String" if field_type == "str" else "Integer"
        lines.append(f"    {field_name} = Column({sql_type})\n")

    model_path.write_text("".join(lines))
