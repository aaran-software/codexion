# cortex/docs/bin/routes.py
from fastapi import APIRouter, HTTPException
from pathlib import Path
import markdown
import yaml

router = APIRouter()

# Docs folder (root)
docs_dir = Path(__file__).parents[3] / "docs"

def build_tree(folder: Path):
    """Recursively build docs tree from _index.yaml."""
    index_file = folder / "_index.yaml"
    items = []

    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            index_data = yaml.safe_load(f) or []

        for entry in sorted(index_data, key=lambda x: x.get("order", 0)):
            slug = entry.get("slug")
            if not slug:
                continue

            entry_path = folder / slug

            # Detect if it's a folder
            if entry_path.is_dir():
                entry["children"] = build_tree(entry_path)
            else:
                entry["children"] = []

            items.append(entry)

    return items


@router.get("/docs")
def docs_index():
    """Return docs structure root."""
    return build_tree(docs_dir)


@router.get("/docs/{slug:path}")
def get_doc(slug: str):
    """Return a single doc as HTML, supports nested paths."""
    md_file = docs_dir / f"{slug}.md"

    if not md_file.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    md_content = md_file.read_text(encoding="utf-8")
    html_content = markdown.markdown(md_content)
    return {"slug": slug, "content": html_content}
