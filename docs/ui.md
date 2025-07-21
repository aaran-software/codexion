from prefiq.utils.ui import print_success, print_error, print_info, print_separator, show_progress

def run(args):
    print_separator("Installing App")

    steps = ["Creating folder", "Writing config", "Finalizing"]
    show_progress("Installing", steps)

    print_success(f"App '{args.name}' installed successfully.")


from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel("Hello, World!", title="Greeting", subtitle="~ rich.panel"))


╭──────────────────── Greeting ────────────────────╮
│ Hello, World!                                    │
╰────────────────────── ~ rich.panel ──────────────╯

╭───────────── prefiq ─────────────╮
│ ✅ Installed successfully        │
╰──────────────────────────────────╯
