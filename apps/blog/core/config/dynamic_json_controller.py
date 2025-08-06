from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from pathlib import Path
from typing import Any, Optional
import json

router = APIRouter(prefix="/json", tags=["DynamicJSON"])

# Root directory to allow only safe access
BASE_PATH = Path(__file__).resolve().parent.parent / "data"

# ======= Models =======
class SectionUpdate(BaseModel):
    data: dict
    filepath: str

class NewSection(BaseModel):
    key: str
    data: dict
    filepath: str

# ======= Helpers =======
def resolve_json_path(filepath: str) -> Path:
    json_path = BASE_PATH / filepath
    if not json_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filepath}' not found")
    if not json_path.is_file():
        raise HTTPException(status_code=400, detail=f"'{filepath}' is not a file")
    return json_path

def read_json_file(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json_file(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ======= Routes =======

@router.get("")
def get_json(filepath: str = Query(..., description="Relative path to JSON file (e.g. 'Blog.json')")):
    try:
        path = resolve_json_path(filepath)
        return read_json_file(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading JSON: {str(e)}")

@router.get("/{section}")
def get_section(
    section: str,
    filepath: str = Query(..., description="Relative path to JSON file"),
):
    try:
        path = resolve_json_path(filepath)
        data = read_json_file(path)
        return data.get("blog", {}).get(section, {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{section}")
def update_section(section: str, body: SectionUpdate):
    try:
        path = resolve_json_path(body.filepath)
        data = read_json_file(path)

        data["blog"][section] = body.data

        write_json_file(path, data)
        return {"message": f"Section '{section}' updated in '{body.filepath}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def add_section(body: NewSection):
    try:
        path = resolve_json_path(body.filepath)
        data = read_json_file(path)

        if body.key in data.get("blog", {}):
            raise HTTPException(status_code=400, detail="Section already exists")

        data.setdefault("blog", {})[body.key] = body.data
        write_json_file(path, data)

        return {"message": f"Section '{body.key}' added to '{body.filepath}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
