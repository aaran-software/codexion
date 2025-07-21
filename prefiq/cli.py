# prefiq/cli.py

import argparse
from prefiq.commands.app import install, uninstall, update_app, list_app, reinstall


def main():
    parser = argparse.ArgumentParser(prog="prefiq", description="Prefiq App Manager")
    subparsers = parser.add_subparsers(dest="command")

    # install-app
    install_parser = subparsers.add_parser("install-app", help="Install a new app")
    install_parser.add_argument("name", help="App name to install")
    install_parser.add_argument("--force", action="store_true", help="Overwrite if app exists")

    # uninstall-app
    uninstall_parser = subparsers.add_parser("uninstall-app", help="Uninstall an app")
    uninstall_parser.add_argument("name", help="App name to uninstall")

    # re-install
    reinstall_parser = subparsers.add_parser("reinstall-app", help="Reinstall an app")
    reinstall_parser.add_argument("name", help="App name to reinstall")

    # update-app
    update_parser = subparsers.add_parser("update-app", help="Update an existing app from Git")
    update_parser.add_argument("name", help="App name to update")

    # list-apps ✅
    list_parser = subparsers.add_parser("list-apps", help="List all installed apps")

    args = parser.parse_args()

    if args.command == "install-app":
        install.run(args)
    elif args.command == "uninstall-app":
        uninstall.run(args)
    elif args.command == "reinstall-app":
        reinstall.run(args)
    elif args.command == "update-app":
        update_app.run(args)
    elif args.command == "list-apps":
        list_app.run([])
    else:
        parser.print_help()
