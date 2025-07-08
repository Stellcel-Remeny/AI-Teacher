#
# This file contains sound file variables
# Use .play() to play
#

# ---[ Libraries ]--- #
from ai_teacher.resources import shared

import pygame
import os

# ---[ Sound setup ]--- #
# Directory
sound_directory: str = os.path.join(shared.app_dir, "media", "sounds")

# Filenames for sound (without path)
# Define new sound filenames here
#
# Todo: make this into a separate txt file
sound_filenames: list[str] = [
    "tick1.wav",
    "tick2.wav"
]

# Dictionary to store loaded pygame Sound objects
# Example use: sounds["tick1"].play()
sounds: dict[str, pygame.mixer.Sound] = {}

# ---[ Init function for sound ]--- #
def init() -> None:
    try:
        pygame.mixer.init()
    except pygame.error as e:
        raise RuntimeError(f"Failed to initialize sound system: {e}")

    if not os.path.isdir(sound_directory):
        raise FileNotFoundError(f"Sound directory not found: {sound_directory}")
    
    for name in sound_filenames:
        if os.path.splitext(name)[1].lower() != ".wav":
            continue  # Skip non-wav files

        full_path = os.path.join(sound_directory, name)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Missing sound file: {full_path}")
        
        sound_name = os.path.splitext(name)[0]  # Remove extension
        sounds[sound_name] = pygame.mixer.Sound(full_path)