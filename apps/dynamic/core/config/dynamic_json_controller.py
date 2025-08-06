import json
import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/config", tags=["Config"])

from pathlib import Path

def load_json_config(json_path: str):
    full_path = Path(__file__).resolve().parent.parent / json_path
    if not full_path.exists():
        raise FileNotFoundError(f"JSON config not found: {json_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_path(file: str) -> Path:
    """Resolve the absolute path to the given JSON config file."""
    path = Path(__file__).resolve().parent.parent / "data" / file
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{file} not found.")
    return path


# def get_nested(data: dict, keys: List[str]):
#     """Traverse nested dictionary with list of keys"""
#     for key in keys:
#         data = data.get(key, {})
#     return data

def get_nested(data: dict, keys: List[str]):
    """Traverse nested dictionary with list of keys"""
    for key in keys:
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail=f"Invalid section path at '{key}'")
        data = data.get(key)
        if data is None:
            return {}
    return data


def set_nested(data: dict, keys: List[str], value: dict):
    """Set value at nested path"""
    d = data
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
    return data


def parse_section_path(section: str) -> List[str]:
    return section.strip().split(".")


class SectionUpdate(BaseModel):
    data: dict


class NewSection(BaseModel):
    section: str  # e.g., "blog.blogs.details"
    data: dict


@router.get("/{file}")
def get_config(file: str):
    """Return the full config from file"""
    try:
        path = resolve_path(file)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error loading {file}: {str(e)}")


@router.get("/{file}/{section:path}")
def get_section(file: str, section: str):
    """Return a nested section"""
    try:
        path = resolve_path(file)
        with open(path, "r") as f:
            config = json.load(f)

        section_keys = parse_section_path(section)
        section_data = get_nested(config, section_keys)
        return section_data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{file}/{section:path}")
def update_section(file: str, section: str, body: SectionUpdate):
    """Update a nested section"""
    try:
        path = resolve_path(file)
        with open(path, "r") as f:
            config = json.load(f)

        section_keys = parse_section_path(section)
        updated = set_nested(config, section_keys, body.data)

        with open(path, "w") as f:
            json.dump(updated, f, indent=2)

        return {"message": f"Section '{section}' updated in {file}"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{file}")
def add_section(file: str, body: NewSection):
    """Add a new nested section"""
    try:
        path = resolve_path(file)
        with open(path, "r") as f:
            config = json.load(f)

        section_keys = parse_section_path(body.section)

        # Check if section already exists
        current = get_nested(config, section_keys)
        if current:
            raise HTTPException(status_code=400, detail=f"Section '{body.section}' already exists.")

        config = set_nested(config, section_keys, body.data)

        with open(path, "w") as f:
            json.dump(config, f, indent=2)

        return {"message": f"Section '{body.section}' added to {file}"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
