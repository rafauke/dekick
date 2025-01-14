"""
Comments
"""
import argparse
import atexit
import logging
import sys
from importlib import import_module
from time import time

from rich.console import Console
from rich.traceback import install

from lib.dekickrc import get_dekick_version
from lib.settings import (
    C_CMD,
    C_CODE,
    C_END,
    C_FILE,
    DEKICK_COMMANDS,
    DEKICK_DOCKER_IMAGE,
    TERMINAL_COLUMN_WIDTH,
    get_dekick_time_start,
    is_dekick_dockerized,
    set_dekick_time_start,
)

install()
console = Console()

set_dekick_time_start()

parser = argparse.ArgumentParser(
    prog="DeKick",
    description="""
DeKick is a provisioning and building application used to run and build applications with
different flavours (languages, frameworks) in local, test, beta and production environments.
""",
)
sub_parser = parser.add_subparsers(required=True, dest="command", help="command to run")

for command in DEKICK_COMMANDS:
    command_parser = sub_parser.add_parser(command, help=f"{command} help")
    module_name = command.replace("-", "_")  # pylint: disable=invalid-name
    module = import_module(f"commands.{module_name}")
    module.arguments(command_parser)

namespace, args = parser.parse_known_args()

version = (
    f"docker:{DEKICK_DOCKER_IMAGE}" if is_dekick_dockerized() else get_dekick_version()
)
print("╭" + ((TERMINAL_COLUMN_WIDTH - 2) * "─") + "╮")

dekick_str_len = len(f"DeKick {namespace.command}")
version_str_len = len(f"version: {version}")

print(
    f"│ {C_CMD}DeKick{C_END} {C_FILE}{namespace.command}"
    + (((TERMINAL_COLUMN_WIDTH - 5) - version_str_len - dekick_str_len) * " ")
    + f"{C_END} version: {C_CODE}{version}{C_END}"
    + " │"
)
print("╰" + ((TERMINAL_COLUMN_WIDTH - 2) * "─") + "╯")


def show_run_time():
    """Shows total the run time of the application."""
    total_run_time = str(round(time() - get_dekick_time_start(), 1))
    print(TERMINAL_COLUMN_WIDTH * "─")
    running_time = f"{C_CMD}DeKick{C_END} was running {C_CODE}{total_run_time} s{C_END}"
    print(running_time)
    logging.info(running_time)


atexit.register(show_run_time)

try:
    namespace.func(namespace, args)
except KeyboardInterrupt:
    sys.stdout.write("\033[2K")
    print("\r  Keyboard interrupted (CTRL+c)")
    sys.exit()
