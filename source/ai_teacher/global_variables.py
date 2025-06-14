#
# Variables & Libraries file for AI Teacher
# Copyright (C) 2025 Remeny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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