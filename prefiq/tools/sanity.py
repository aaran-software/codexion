# tools/sanity.py
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root (../.. from tools/)
PKG  = ROOT / "prefiq"
CLI  = PKG / "cli"
PYPROJECT = ROOT / "pyproject.toml"

GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; RESET = "\033[0m"

def info(msg):  print(f"{GREEN}✔{RESET} {msg}")
def warn(msg):  print(f"{YELLOW}!{RESET} {msg}")
def err(msg):   print(f"{RED}✖{RESET} {msg}")

def ensure_inits(paths: list[Path]) -> list[Path]:
    created: list[Path] = []
    for p in paths:
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("", encoding="utf-8")
            created.append(p)
    return created

def detect_cli_layout():
    flat = (CLI / "server.py").exists() and (CLI / "database.py").exists()
    nested = (CLI / "server" / "cli.py").exists() and (CLI / "database" / "cli.py").exists()
    if flat and nested:
        warn("Both flat and nested CLI layouts detected; defaulting to FLAT.")
        return "flat"
    if flat:
        return "flat"
    if nested:
        return "nested"
    return "unknown"

FLAT_MAIN = """\
from __future__ import annotations
import typer
from prefiq.cli import server, database

app = typer.Typer(help="Prefiq CLI entrypoint")
app.add_typer(server.app, name="server")   # prefiq server run
app.add_typer(database.app, name="run")    # prefiq run migrate

def main():
    app()

if __name__ == "__main__":
    main()
"""

NESTED_MAIN = """\
from __future__ import annotations
import typer
from prefiq.cli.server.cli import app as server_app
from prefiq.cli.database.cli import app as db_app

app = typer.Typer(help="Prefiq CLI entrypoint")
app.add_typer(server_app, name="server")   # prefiq server run
app.add_typer(db_app,     name="run")      # prefiq run migrate

def main():
    app()

if __name__ == "__main__":
    main()
"""

def write_main_cli(layout: str) -> bool:
    target = CLI / "main_cli.py"
    desired = FLAT_MAIN if layout == "flat" else NESTED_MAIN
    if not target.exists() or target.read_text(encoding="utf-8").strip() != desired.strip():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(desired, encoding="utf-8")
        return True
    return False

def patch_pyproject() -> list[str]:
    """
    Ensures:
      - [project.scripts] prefiq = "prefiq.cli.main_cli:main"
      - typer>=0.12 present in [project].dependencies
    Returns list of changes.
    """
    changes: list[str] = []
    if not PYPROJECT.exists():
        err("pyproject.toml not found; skipping.")
        return changes

    text = PYPROJECT.read_text(encoding="utf-8")

    # 1) Ensure console script
    scripts_block_re = re.compile(r"(?ms)^\\[project\\.scripts\\][^\\[]*")
    if "[project.scripts]" not in text:
        text += '\n\n[project.scripts]\nprefiq = "prefiq.cli.main_cli:main"\n'
        changes.append('added [project.scripts] prefiq = "prefiq.cli.main_cli:main"')
    else:
        block = scripts_block_re.search(text)
        if block:
            blk = block.group(0)
            if 'prefiq =' not in blk:
                blk_new = blk.rstrip() + '\nprefiq = "prefiq.cli.main_cli:main"\n'
                text = text.replace(blk, blk_new)
                changes.append('set prefiq console script -> "prefiq.cli.main_cli:main"')
            else:
                # replace existing prefiq line
                blk_new = re.sub(r'(?m)^\s*prefiq\s*=\s*".*"$',
                                 'prefiq = "prefiq.cli.main_cli:main"', blk)
                if blk_new != blk:
                    text = text.replace(blk, blk_new)
                    changes.append('updated prefiq console script -> "prefiq.cli.main_cli:main"')

    # 2) Ensure typer dep
    deps_re = re.compile(r"(?ms)^\\[project\\]\\s.*?^dependencies\\s*=\\s*\\[(.*?)\\]", re.DOTALL)
    m = deps_re.search(text)
    if not m:
        # Add a dependencies list if missing
        text = re.sub(r"(?ms)^\\[project\\][^\\[]*",
                      lambda mm: mm.group(0).rstrip() + '\n\ndependencies = [\n  "typer>=0.12",\n]\n',
                      text, count=1)
        changes.append('added [project].dependencies with typer>=0.12')
    else:
        deps_block = m.group(0)
        inner = m.group(1)
        if "typer" not in inner:
            deps_block_new = deps_block.replace(inner, (inner + '\n  "typer>=0.12",\n'))
            text = text.replace(deps_block, deps_block_new)
            changes.append('added typer>=0.12 to [project].dependencies')

    if changes:
        PYPROJECT.write_text(text, encoding="utf-8")
    return changes

def run(fix: bool = True) -> int:
    if not PKG.exists():
        err(f"Package folder not found: {PKG}")
        return 1

    # 1) Detect layout
    layout = detect_cli_layout()
    if layout == "unknown":
        err("Could not detect CLI layout. Expected either flat (cli/server.py & cli/database.py) "
            "or nested (cli/server/cli.py & cli/database/cli.py).")
        return 2
    info(f"Detected CLI layout: {layout.upper()}")

    # 2) Ensure __init__.py files
    inits = [PKG / "__init__.py", CLI / "__init__.py"]
    if layout == "nested":
        inits += [CLI / "server" / "__init__.py", CLI / "database" / "__init__.py"]
    created = ensure_inits(inits)
    if created:
        info(f"Created {len(created)} __init__.py file(s)")
        for c in created:
            print(f"   - {c.relative_to(ROOT)}")
    else:
        info("All required __init__.py files present")

    # 3) Ensure main_cli matches layout
    if fix:
        wrote = write_main_cli(layout)
        if wrote:
            info("Rewrote cli/main_cli.py to match layout")
        else:
            info("cli/main_cli.py already matches layout")

    # 4) Patch pyproject.toml
    changes = patch_pyproject()
    if changes:
        info("Updated pyproject.toml:")
        for c in changes:
            print(f"   - {c}")
    else:
        info("pyproject.toml already OK")

    # 5) Final hints
    print()
    print("Next steps:")
    print("  1) Reinstall entry point:  pip install -e .")
    print("  2) Try:                    prefiq server run")
    print("  3) Try:                    prefiq run migrate --seed")
    return 0

if __name__ == "__main__":
    code = run(fix=True)
    sys.exit(code)
