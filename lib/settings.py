from getpass import getuser
from os import get_terminal_size, getcwd, getenv, getuid
from sys import stdout
from time import time

from lib.terminal_colors import TerminalColors

colors = TerminalColors()

DEKICK_MASTER_VERSION_URL = (
    "https://raw.githubusercontent.com/DeSmart/dekick/main/.version"
)
DEKICK_GIT_URL = "https://github.com/DeSmart/dekick.git"
DEKICK_BOILERPLATES = [
    "api/node/js",
    "api/node/ts",
    "api/php/7.4",
    "api/php/8.0",
    "api/php/8.1",
    "front/react/generic",
    "mono/vue/8.0",
    "front/vue/deauth",
]
DEKICK_FLAVOURS = ["express", "react", "laravel"]

# Available commands to use with dekick
# Warning! If you add a new command, you must add it to ./docker/docker-entrypoint.sh also!
DEKICK_COMMANDS = [
    "artisan",
    "build",
    "composer",
    "docker-compose",
    "knex",
    "local",
    "logs",
    "node",
    "npm",
    "npx",
    "phpunit",
    "pint",
    "seed",
    "status",
    "stop",
    "test",
    "update",
    "yarn",
]

C_CMD = colors.fg("purple")
C_CODE = colors.fg("orange")
C_END = colors.reset()
C_FILE = colors.fg("lightcyan")
C_BOLD = colors.bold()
C_ERROR = colors.fg("red")
C_WARN = colors.fg("yellow")

PROJECT_ROOT = getenv("PROJECT_ROOT") or f"{getcwd()}"
DEKICK_PATH = getenv("DEKICK_PATH") or f"{getcwd()}/dekick"
DEKICK_DOCKER_IMAGE = getenv("DEKICK_DOCKER_IMAGE") or None
CURRENT_UID = str(getenv("CURRENT_UID") or getuid())
CURRENT_USERNAME = getenv("CURRENT_USERNAME") or getuser()
TERMINAL_COLUMN_WIDTH = (get_terminal_size().columns - 3) if stdout.isatty() else 120

DEKICKRC_TMPL_FILE = ".dekickrc.tmpl.yml"
DEKICKRC_FILE = ".dekickrc.yml"

DEKICKRC_TMPL_PATH = f"{DEKICK_PATH}/{DEKICKRC_TMPL_FILE}"
DEKICKRC_PATH = f"{PROJECT_ROOT}/{DEKICKRC_FILE}"

DEKICK_VERSION_FILE = ".version"
DEKICK_VERSION_PATH = f"{DEKICK_PATH}/{DEKICK_VERSION_FILE}"

DEKICK_MIGRATIONS_DIR = f"{DEKICK_PATH}/migrations"

DEKICK_DOTENV_FILE = ".env"
DEKICK_DOTENV_PATH = f"{PROJECT_ROOT}/{DEKICK_DOTENV_FILE}"

DEKICK_TIME_START = 0

DEKICK_PYTEST_MODE = False

DEKICK_CI_MODE = False


def set_dekick_time_start():
    """Update DEKICK_TIME_START"""
    global DEKICK_TIME_START  # pylint: disable=global-statement
    DEKICK_TIME_START = time()


def get_dekick_time_start() -> float:
    """Get DEKICK_TIME_START"""
    return DEKICK_TIME_START


def get_seconds_since_dekick_start() -> int:
    """Get seconds since dekick start"""
    return int(round(time() - get_dekick_time_start()))


def is_dekick_dockerized() -> bool:
    """Check if DeKick is running inside a Docker container"""
    return bool(getenv("DEKICK_DOCKER_IMAGE")) or False


def set_pytest_mode(mode: bool):
    """Sets DEKICK_PYTEST_MODE to True"""
    global DEKICK_PYTEST_MODE  # pylint: disable=global-statement
    DEKICK_PYTEST_MODE = mode


def is_pytest() -> bool:
    """Check if DeKick is running inside a Docker container"""
    return DEKICK_PYTEST_MODE


def set_ci_mode(mode: bool):
    """Sets DEKICK_CI_MODE to True"""
    global DEKICK_CI_MODE  # pylint: disable=global-statement
    DEKICK_CI_MODE = mode


def is_ci() -> bool:
    """Check if DeKick is running in CI/CD environment"""
    return DEKICK_CI_MODE
