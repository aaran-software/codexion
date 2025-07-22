
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# ─────────────────────────────────────────────────────
# Basic Colored Messages
# ─────────────────────────────────────────────────────

def cprint_success(message: str):
    console.print(f"[bold green][OK][/bold green] {message}")

def cprint_error(message: str):
    console.print(f"[bold red][ERROR][/bold red] {message}")

def cprint_warning(message: str):
    console.print(f"[bold yellow][WARN][/bold yellow] {message}")

def cprint_info(message: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")

def cprint_separator(title: str = ""):
    console.rule(f"[bold blue]{title}[/bold blue]" if title else "")

def cprint_alert(message: str):
    print(f"[bold red]Alert![/bold red] [white]{message}[/white]! :boom:")
