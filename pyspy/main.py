# !/usr/local/bin/python3.6
# MIT licensed
# Copyright (c) 2018 White Russsian
# Github: <https://github.com/Eve-PySpy/PySpy>**********************
''' This is the primary module responsible for launching a background
thread that watches for changes in the clipboard and if it detects a
list of strings that could be EVE Online character strings, sends them
to the analyze.py module to gather specific information from CCP's ESI
API and zKIllboard's API. This information then gets sent to the GUI for
output.
'''
# **********************************************************************
import logging
import re
import threading
import time

import wx
import pyperclip

from . import analyze
from . import chkversion
from . import gui
from . import statusmsg
from . import db
# cSpell Checker - Correct Words****************************************
# // cSpell:words russsian, ccp's, pyperclip, chkversion, clpbd, gui
# **********************************************************************
Logger = logging.getLogger(__name__)
# Example call: Logger.info("Something badhappened", exc_info=True) ****

app = None


def watch_clpbd(myapp):
    try:
        Logger.info("Launched clipboard watcher")
        valid = False
        recent_value = None
        while True:
            clipboard = pyperclip.paste()
            if clipboard != recent_value:
                char_names = clipboard.splitlines()
                if len(char_names) > 3500:
                    statusmsg.push_status(
                        "Skipped excesssively long list of pilots", myapp)
                for name in char_names:
                    valid = check_name_validity(name)
                    if valid is False:
                        statusmsg.push_status(
                            f"Ignored invalid charnames due to {name}", myapp)
                        break
                if valid:
                    statusmsg.push_status(
                        "Clipboard change detected...", myapp)
                    recent_value = clipboard
                    analyze_chars(clipboard.splitlines(), myapp)
            time.sleep(0.5)  # Short sleep between loops to reduce CPU load
    except Exception as e:
        Logger.exception(e)


def check_name_validity(char_name):
    if len(char_name) < 3 or len(char_name) > 37 or char_name.count(' ') > 2:
        return False
    regex = r"[^ 'a-zA-Z0-9-]"  # Valid EVE Online character names
    if re.search(regex, char_name):
        return False
    return True


def analyze_chars(char_names, app):
    conn_mem, cur_mem = db.connect_memory_db()
    conn_dsk, cur_dsk = db.connect_persistent_db()
    start_time = time.time()
    wx.CallAfter(app.PySpy.grid.ClearGrid)
    try:
        outlist = analyze.main(
            char_names,
            conn_mem,
            cur_mem,
            conn_dsk,
            cur_dsk, app)
        duration = round(time.time() - start_time, 1)
        if outlist is not None:
            # Need to use keyword args as sortOutlist can also get called
            # by event handler which would pass event object as first argument.
            wx.CallAfter(
                app.PySpy.sortOutlist,
                outlist=outlist,
                duration=duration
            )
        else:
            statusmsg.push_status(
                "No valid character names found. Please try again...", app
            )
    except Exception as e:
        Logger.exception(
            "Failed to collect character information. Clipboard "
            "content was: " + str(char_names), exc_info=True
        )


def main():
    global app
    # Has to be defined before background thread starts.
    app = gui.App()
#    app = gui.App(redirect=True, filename="pyspy.log")

    background_thread = threading.Thread(
        target=watch_clpbd,
        args=(app,),
        daemon=True
    )
    background_thread.start()

    update_checker = threading.Thread(
        target=chkversion.chk_github_update,
        args=(app,),
        daemon=True
    )
    update_checker.start()

    app.MainLoop()
