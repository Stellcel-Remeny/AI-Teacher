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

# ---[ Shared variables type ]--- #
config: ConfigParser
init_time_formatted: datetime

init_time: float

build_number: int = 0

config_file: str = ""
app_dir: str = ""
version: str = ""
user_name: str = ""
user_dir: str = ""