"""BobsiMo Timer: A simple timer app to manage your kids computer time

"""

import os
import tkinter as tk
import json
import pathlib
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import time

__all__ = ['app_icon',
             'tk','time','json', 'pathlib', 'threading', 'messagebox', 'os',
               'ScrolledText', 'app_name', 'VERSION','computer']


VERSION = "1.3.0"

app_name = f"BobsiMo Timer {VERSION}"


# NOTE This is for production only
# PRODUCTION
app_icon = "./_internal/appdata/imgs/BMT_logo.ico"

# NOTE: Use this in development instead
#  but comment out before production
# DEV
# app_icon = "BMT_logo.ico"


# this is for debugging purpose
# try:
#    logfile = open('./log.txt', 'a')
# except PermissionError:
#    pass


# NOTE 1: when a person wants to create a profile, the window for
# profile creation goes to the back because the focus changes

# TODO: MUST add menus for feedback area (DONE: 051024)
# TODO: remove feature of free creation of profiles
# URGENT TODO: Add the feature to manage the screen time. upfront.


# NOTE: Production directory for profiles
# it shouldn't be plain to anyone
# PRODUCTION
computer = os.getenv(f'USERPROFILE')




