# !/usr/local/bin/python3.6
# MIT licensed
# Copyright (c) 2018 White Russsian
# Github: <https://github.com/jhmartin/PySpy>**********************
''' This module provides connectivity to CCP's ESI API, to zKillboard's
API and to PySpy's own proprietary RESTful API.
'''
# **********************************************************************
import json
import logging
import threading
import time

import requests

import statusmsg
# cSpell Checker - Correct Words****************************************
# // cSpell:words wrusssian, ZKILL, gmail, blops, toon, HICs, russsian,
# // cSpell:words ccp's, activepvp
# **********************************************************************
Logger = logging.getLogger(__name__)
# Example call: Logger.info("Something badhappened", exc_info=True) ****


# ESI Status
# https://esi.evetech.net/ui/?version=meta#/Meta/get_status

def post_req_ccp(esi_path, json_data):
    url = "https://esi.evetech.net/latest/" + esi_path + \
        "?datasource=tranquility"
    try:
        r = requests.post(url, json_data, timeout=30)
    except requests.exceptions.ConnectionError:
        Logger.info("No network connection.", exc_info=True)
        statusmsg.push_status(
            "NETWORK ERROR: Check your internet connection and firewall settings."
        )
        time.sleep(5)
        return "network_error"
    if r.status_code != 200:
        server_msg = json.loads(r.text)["error"]
        Logger.info(
            "CCP Servers at (" + esi_path + ") returned error code: " +
            str(r.status_code) + ", saying: " + server_msg, exc_info=True
        )
        statusmsg.push_status(
            "CCP SERVER ERROR: " + str(r.status_code) + " (" + server_msg + ")"
        )
        return "server_error"
    return r.json()


class Query_zKill(threading.Thread):
    # Run in a separate thread to query certain kill board statistics
    # from zKillboard's API and return the values via a queue object.
    def __init__(self, char_id, q):
        super(Query_zKill, self).__init__()
        self.daemon = True
        self._char_id = char_id
        self._queue = q

    def run(self):
        url = (
            "https://zkillboard.com/api/stats/characterID/" +
            str(self._char_id) + "/"
        )
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": "PySpy, jhmartin@toger.us"
        }
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            Logger.info("No network connection.", exc_info=True)
            statusmsg.push_status(
                '''NETWORK ERROR: Check your internet connection
                and firewall settings.'''
            )
            time.sleep(5)
            return "network error"
        if r.status_code != 200:
            server_msg = "N/A"
            try:
                server_msg = json.loads(r.text)["error"]
            except BaseException:
                pass
            Logger.info(
                "zKillboard server returned error for character ID " +
                str(self._char_id) + ". Error code: " + str(r.status_code),
                exc_info=True
            )
            statusmsg.push_status(
                "ZKILL SERVER ERROR: " +
                str(r.status_code) + " (" + server_msg + ")"
            )
            return "server error"
        try:
            r = r.json()
        except AttributeError:
            kills = 0
            blops_kills = 0
            hic_losses = 0
            self._queue.put([kills, blops_kills, self._char_id])
            return

        try:
            # Number of total kills
            kills = r["shipsDestroyed"]
        except (KeyError, TypeError):
            kills = 0

        try:
            # Number of BLOPS killed
            blops_kills = r["groups"]["898"]["shipsDestroyed"]
        except (KeyError, TypeError):
            blops_kills = 0

        try:
            # Number of HICs lost
            hic_losses = r["groups"]["894"]["shipsLost"]
        except (KeyError, TypeError):
            hic_losses = 0

        try:
            # Kills over past 7 days
            week_kills = r["activepvp"]["kills"]["count"]
        except (KeyError, TypeError):
            week_kills = 0

        try:
            # Number of total losses
            losses = r["shipsLost"]
        except (KeyError, TypeError):
            losses = 0

        try:
            # Ratio of solo kills to total kills
            solo_ratio = int(r["soloKills"]) / int(r["shipsDestroyed"])
        except (KeyError, TypeError):
            solo_ratio = 0

        try:
            # Security status
            sec_status = r["info"]["secStatus"]
        except (KeyError, TypeError):
            sec_status = 0

        self._queue.put(
            [kills, blops_kills, hic_losses, week_kills, losses, solo_ratio,
             sec_status, self._char_id]
        )
        return


def post_proprietary_db(character_ids):
    '''
    Query PySpy's proprietary kill database for the character ids
    provided as a list or tuple of integers. Returns a list of JSON dicts
    with results. We use GET / just one id at a time for CDN cachability.

    :param `character_ids`: List or tuple of character ids as integers.
    :return: Array containing  statistics for each id.
    '''
    url = "https://pyspy.toger.us/v2/character_intel"
    headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "PySpy, https://github.com/jhmartin/PySpy"
    }
    # Character_ids is a list of tuples, which needs to be converted to dict
    # with list as value.
    results = []
    for character_id in character_ids:
        try:
            r = requests.get(
                url, headers=headers, params={
                    'character_id': character_id}, timeout=10)
        except requests.exceptions.ConnectionError as e:
            Logger.info("No network connection.", exc_info=True)
            statusmsg.push_status(
                "NETWORK ERROR: Check your internet connection and firewall settings."
            )
            time.sleep(5)
            raise e
        if r.status_code != 200:
            server_msg = r.text
            Logger.info(
                "PySpy server returned error code: " +
                str(r.status_code) + ", saying: " + server_msg, exc_info=True
            )
            statusmsg.push_status(
                "PYSPY SERVER ERROR: " +
                str(r.status_code) + " (" + server_msg + ")"
            )
            return "server_error"
        results.append(r.json())
    return results


def get_ship_data():
    '''
    Produces a list of ship id and ship name pairs for each ship in EVE
    Online, precalculated and loaded onto the pyspy servers.

    :return: List of lists containing ship ids and related ship names.
    '''
    url = "https://pyspy.toger.us/static/shipnames.json"
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError as e:
        Logger.error("[get_ship_data] No network connection.", exc_info=True)
        raise e
    if r.status_code != 200:
        server_msg = json.loads(r.text)["error"]
        Logger.error(
            "[get_ship_data] Pyspy servers returned error code: " +
            str(r.status_code) + ", saying: " + server_msg, exc_info=True
        )
        raise Exception("server_error")
    return r.json()
