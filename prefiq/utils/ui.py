# prefiq/utils/ui.py

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

console = Console()


def print_success(message):
    console.print(f"[bold green][OK][/bold green] {message}")

def print_error(message):
    console.print(f"[bold red][ERROR][/bold red] {message}")

def print_warning(message):
    console.print(f"[bold yellow][WARN][/bold yellow] {message}")

def print_info(message):
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")

def print_separator(title: str = ""):
    console.rule(f"[bold blue]{title}[/bold blue]" if title else "")


def show_progress(task_message: str, steps: list[str]):
    with Progress() as progress:
        task = progress.add_task(task_message, total=len(steps))
        for step in steps:
            progress.update(task, advance=1)
            console.print(f"[green]*[/green] {step}")
