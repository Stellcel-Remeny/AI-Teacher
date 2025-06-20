#
# Shared variables & Libraries file for AI Teacher
# Copyright (C) 2025 Remeny
#

# ---[ Libraries ]--- #
from datetime import datetime
import time
import os
import platform

# ---[ Global Variable definitions ]--- #
init_time: int = time.time()
init_time_formatted: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

BuildNumberFile: str = "./resources/build.txt" # File that holds how much builds have passed
user_settings_file: str = "./data/settings.env" # Environmental file for user configuration

development: bool = True
debug: bool = True

# ---[ Version ]--- #

MajorVersion: int = 0
MinorVersion: int = 0
AlphaRelease: int = 1
DefaultBuildNumber: int = 1

version: str
codename: str = "The Fun They Had"