# Markdown loading and parsing service
import markdown
from pathlib import Path

def load_markdown(slug):
    md_file = Path(__file__).parent.parent / 'content' / f"{slug}.md"
    if md_file.exists():
        return markdown.markdown(md_file.read_text())
    return None