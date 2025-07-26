import traceback
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
import json

router = APIRouter(prefix="/config", tags=["Config"])

INVOICE_PATH = Path(__file__).resolve().parent.parent / "data" / "Invoice.json"
print("Resolved path:", INVOICE_PATH)
print("File exists:", INVOICE_PATH.exists())

@router.get("/invoice")
def get_invoice_config():
    try:
        with open(INVOICE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading invoice config: {str(e)}")
@router.get("/invoice/{section}")
def get_section(section: str):
    try:
        with open(INVOICE_PATH, "r") as f:
            data = json.load(f)
        return data["invoice"].get(section, {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SectionUpdate(BaseModel):
    data: dict

@router.put("/invoice/{section}")
def update_section(section: str, body: SectionUpdate):
    try:
        with open(INVOICE_PATH, "r") as f:
            config = json.load(f)

        config["invoice"][section] = body.data

        with open(INVOICE_PATH, "w") as f:
            json.dump(config, f, indent=2)

        return {"message": f"{section} updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class NewSection(BaseModel):
    key: str
    data: dict

@router.post("/invoice")
def add_section(body: NewSection):
    try:
        with open(INVOICE_PATH, "r") as f:
            config = json.load(f)

        if body.key in config["invoice"]:
            raise HTTPException(status_code=400, detail="Section already exists")

        config["invoice"][body.key] = body.data

        with open(INVOICE_PATH, "w") as f:
            json.dump(config, f, indent=2)

        return {"message": f"Section {body.key} added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
