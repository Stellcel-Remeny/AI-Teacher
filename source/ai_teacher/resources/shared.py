#
# Contains global variables that python files can use
# to communicate. Variables can be manually added or
# loaded from configuration.ini
#

global config, config_file, app_dir, version, init_time, init_time_formatted, build_number
global user_dir

# ---[ Stuff needed to declare type ]--- #
from configparser import ConfigParser
from datetime import datetime
from customtkinter import CTk # type: ignore

# ---[ Shared variables ]--- #
config: ConfigParser  = ConfigParser()
user_config: ConfigParser = ConfigParser()

init_time_formatted: datetime | None = None

root_app: CTk | None = None

debug: bool = False
log: bool = False

init_time: float = 0.0

build_number: int = 0

config_file: str = ""
user_config_file: str = ""
app_dir: str = ""
version: str = ""
user_name: str = ""
user_dir: str = ""