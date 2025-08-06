import traceback
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
import json

router = APIRouter(prefix="/config", tags=["Config"])

BLOG_PATH = Path(__file__).resolve().parent.parent / "data" / "Blog.json"
print("Resolved path:", BLOG_PATH)
print("File exists:", BLOG_PATH.exists())

@router.get("/blog")
def get_blog_config():
    try:
        with open(BLOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading invoice config: {str(e)}")
@router.get("/blog/{section}")
def get_section(section: str):
    try:
        with open(BLOG_PATH, "r") as f:
            data = json.load(f)
        return data["blog"].get(section, {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SectionUpdate(BaseModel):
    data: dict

@router.put("/blog/{section}")
def update_section(section: str, body: SectionUpdate):
    try:
        with open(BLOG_PATH, "r") as f:
            config = json.load(f)

        config["blog"][section] = body.data

        with open(BLOG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        return {"message": f"{section} updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class NewSection(BaseModel):
    key: str
    data: dict

@router.post("/blog")
def add_section(body: NewSection):
    try:
        with open(BLOG_PATH, "r") as f:
            config = json.load(f)

        if body.key in config["blog"]:
            raise HTTPException(status_code=400, detail="Section already exists")

        config["blog"][body.key] = body.data

        with open(BLOG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        return {"message": f"Section {body.key} added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
