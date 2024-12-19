# !/usr/local/bin/python3.6
# MIT licensed
# Copyright (c) 2018 White Russsian
# Github: <https://github.com/Eve-PySpy/PySpy>**********************
''' Checks if there is a later version of PySpy available on GitHub.'''
# **********************************************************************
import logging.config
import logging
import datetime

import requests
import wx

import __main__
import config
# cSpell Checker - Correct Words****************************************
# // cSpell:words russsian
# **********************************************************************
Logger = logging.getLogger(__name__)
# Example call: Logger.info("Something badhappened", exc_info=True) ****
CURRENT_VER = config.CURRENT_VER


def chk_github_update():
    last_check = config.OPTIONS_OBJECT.Get("last_update_check", 0)
    if last_check == 0 or last_check < datetime.date.today():
        # Get latest version available on GitHub
        git_url = "https://api.github.com/repos/jhmartin/PySpy/releases/latest"
        try:
            # verify=False to avoid certificate errors. This is not critical.
            latest_ver = requests.get(git_url, timeout=5).json()["tag_name"]
            Logger.info(
                "You are running " + CURRENT_VER + " and " +
                latest_ver + " is the latest version available on GitHub."
                )
            config.OPTIONS_OBJECT.Set("last_update_check", datetime.date.today())
            if latest_ver != CURRENT_VER:
                wx.CallAfter(__main__.app.PySpy.updateAlert, latest_ver, CURRENT_VER)
        except:
            Logger.info("Could not check GitHub for potential available updates.")
