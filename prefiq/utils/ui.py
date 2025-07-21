# prefiq/utils/ui.py

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

def print_success(message: str):
    console.print(f"[bold green][OK][/bold green] {message}")


def print_error(message: str):
    console.print(f"[bold red][ERROR][/bold red] {message}")


def print_warning(message: str):
    console.print(f"[bold yellow][WARN][/bold yellow] {message}")


def print_info(message: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")


def print_separator(title: str = ""):
    """Draw a horizontal rule with an optional title."""
    console.rule(f"[bold blue]{title}[/bold blue]" if title else "")


def _alert(message: str):
    print(f"[bold red]Alert![/bold red] [white]{message}[/white]! :boom:")


# ─────────────────────────────────────────────────────
# Panel Helpers
# ─────────────────────────────────────────────────────

def panel_message(message: str, title: str = "Message", style: str = "bold white", border_style: str = "cyan",
                  box_style=box.ROUNDED):
    """Prints a panel with custom styles."""
    panel = Panel(Text(message, style=style), title=title, border_style=border_style, box=box_style)
    console.print(panel)


def panel_success(message: str, title="Success"):
    panel_message(message, title, style="bold green", border_style="green")


def panel_error(message: str, title="Error"):
    panel_message(message, title, style="bold red", border_style="red")


def panel_info(message: str, title="Info"):
    panel_message(message, title, style="bold cyan", border_style="cyan")


def panel_warning(message: str, title="Warning"):
    panel_message(message, title, style="bold yellow", border_style="yellow")


# ─────────────────────────────────────────────────────
# Progress Bar
# ─────────────────────────────────────────────────────

def show_progress(task_message: str, steps: list[str]):
    """Displays a progress bar with step logging."""
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=True
    ) as progress:
        task = progress.add_task(task_message, total=len(steps))
        for step in steps:
            progress.console.print(f"[green]•[/green] {step}")
            progress.update(task, advance=1)


# ─────────────────────────────────────────────────────
#  Text Style Utility
# ─────────────────────────────────────────────────────

from rich.text import Text


def styled_text(content: str, color: str = "white", bold: bool = False, italic: bool = False) -> Text:
    """Returns a styled Text object with the specified color and optional bold/italic styles."""
    style_parts = []
    if bold:
        style_parts.append("bold")
    if italic:
        style_parts.append("italic")
    style_parts.append(color)

    style_str = " ".join(style_parts)
    return Text(content, style=style_str)


def print_main_help():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("install-app", "Install a new app")
    table.add_row("uninstall-app", "Uninstall an app")
    table.add_row("reinstall-app", "Reinstall an app")
    table.add_row("update-app", "Update an existing app from Git")
    table.add_row("list-apps", "List all installed apps")

    panel = Panel(
        table,
        title="[bold cyan]Prefiq App Manager[/bold cyan]",
        subtitle="Use [bold yellow]prefiq <command> --help[/bold yellow] for more info.",
        border_style="cyan",
    )

    console.print(panel)


"""
from prefiq.utils.ui import *

print_success("App installed successfully!")
print_error("Failed to install dependency.")
print_warning("Low disk space.")
print_info("Checking latest version...")

panel_success("All systems operational.")
panel_error("App crashed on startup.")
panel_info("Version 1.0.2 now available.")
panel_warning("Unsupported config detected.")

print_separator("Install Report")

show_progress("Installing components", ["Fetching template", "Copying files", "Creating config", "Finalizing"])

console.print(styled_text("This is styled text!", color="magenta", bold=True, italic=True))

console.print(styled_text("Green Bold", color="green", bold=True))
console.print(styled_text("Red Italic", color="red", italic=True))
console.print(styled_text("Blue Normal", color="blue"))
console.print(styled_text("Orange Bold Italic", color="orange", bold=True, italic=True))


"""
