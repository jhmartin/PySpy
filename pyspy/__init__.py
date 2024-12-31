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
