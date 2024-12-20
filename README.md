<!--- // cSpell:words killboard, blops, hics, killboard's, cynos, ccp's, pyspy, psf's, pyperclip, pyinstaller, executables, jojo, unported, killmails --->

# PySpy - A simple EVE Online character intel tool using CCP's ESI API

<p align="left">
  <a href=https://github.com/jhmartin/PySpy/releases/latest>
    <img alt="Current Version" src="https://img.shields.io/github/release/jhmartin/pyspy.svg">
  </a>
  <a href=https://github.com/jhmartin/PySpy/releases/latest>
    <img alt="Number of releases downloaded" src="https://img.shields.io/github/downloads/jhmartin/PySpy/total.svg">
  </a>
</p>

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/jhmartin/PySpy/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/jhmartin/PySpy/tree/master)

**Download the latest release [here](https://github.com/jhmartin/PySpy/releases/latest).**

## Background

PySpy is a fast and simple character intel tool for [EVE Online](https://www.eveonline.com/). Within seconds, PySpy gathers useful information on character names from the in-game *local chat* window.

PySpy connects to [CCP's ESI API](https://esi.evetech.net/ui/) and the
[zKillboard API](https://github.com/zKillboard/zKillboard/wiki) and is available on Windows, macOS and Linux.

In addition, PySpy uses a proprietary database which creates summary statistics for approximately 2.4 million EVE Online pilots, based on some 50 million killmails dating back to December 2007. This database is updated daily, shortly after CCP server downtime.

If you enjoy using PySpy and would like to show your appreciation, please feel free to send ISK in-game to White Russsian (with 3 's'). Thank you.

## How to use PySpy

1. Open PySpy.
2. In your EVE client, select a list of characters and copy them to the clipboard (`CTRL+C` on Windows *or* `⌘+C` on macOS).
3. Wait until PySpy is done and inspect the results.
4. Double-click a name to open the respective zKillboard in your browser. zKillboard will open to the relevant page based on the column you have clicked on. (Or to the character page if you turn off advanced zkillboard linking)

**Note**: PySpy will save its window location, size, column sizes, sorting order and transparency (slider on bottom right) and any other settings automatically and restore them the next time you launch it (settings will be reset whenever you update to a new version). If selected in the _View Menu_, PySpy will stay on top of the EVE client so long as the game runs in *window mode*.

## Information Provided by PySpy

### New Dark Mode
<p align="center">
  <img alt="PySpy in action" src="https://github.com/jhmartin/PySpy/blob/master/assets/v0.4_dark_screenshot.png?raw=true">
</p>

### Traditional Normal Mode
<p align="center">
  <img alt="PySpy in action" src="https://github.com/jhmartin/PySpy/blob/master/assets/v0.4_light_screenshot.png?raw=true">
</p>

* **Warning**: Displays reasons why a character might be highlighted
* **Character**: Character name.
* **Security**: Concord security status.
* **Corporation**: Corporation of character.
* **Alliance**: Alliance of character's Corporation, if any.
* **Faction**: Faction of character, if any.
* **Kills**: Total number of kills.
* **Losses**: Total number of losses.
* **Last Wk**: Number of kills over past 7 days.
* **Solo**: Ratio of solo kills over total kills.
* **BLOPS**: Number of Black Ops Battleships (BLOPS) killed.
* **HICs**: Number of lost Heavy Interdiction Cruisers (HIC).
* **Last Loss**: Days since last loss.
* **Last Kill**: Days since last kill.
* **Avg. Attackers**: Average number of attackers per kill.
* **Covert Cyno**: Ratio of losses where a covert cyno was fitted to total losses.
* **Regular Cyno**: Ratio of losses where a regular cyno was fitted to total losses.
* **Last Covert Cyno**: Ship type of most recent loss where covert cyno was fitted.
* **Last Regular Cyno**: Ship type of most recent loss where regular cyno was fitted.
* **Abyssal Losses**: Number of ship losses in Abyssal space.

**Current Limitations**: To avoid undue strain on zKillboard's API, PySpy will run the *Kills*, *Losses*, *Last Wk*, *Solo*, *BLOPS* and *HICs* analyses only for the first 100 characters in the list.

## Ignore Certain Entities

PySpy allows you to specify a list of ignored characters, corporations and alliances. To add entities to that list, right click on a search result. You can remove entities from this list under _Options_->_Review Ignored Entities_.

## Ignore all Members of your NPSI Fleet

For anyone using PySpy in not-purple-shoot-it (NPSI) fleets, you can tell PySpy to temporarily ignore your fleet mates by first running PySpy on all characters in your fleet chat and then selecting _Options_->_Set NPSI Ignore List_. Once the fleet is over, you can clear the list under _Options_->_Clear NPSI List_. Your custom ignore list described above will not be affected by this action.

## Highlighting

PySpy allows you to specify a list of highlighted characters, corporations and alliances.
These entities will be highlighted in a different color from the others.
To add and remove entities to that list, right click on a search result.
You can also review and remove entities from this list under _Options_->_Review Highlighted Entities_.

Furthermore PySpy can also highlight a character if he uses Black Ops and Heavy Interdiction Cruisers or frequently has a cyno fitted.

## Installation

You can download the latest release for your operating system [here](https://github.com/Eve-PySpy/PySpy/releases/latest).

PySpy comes as a single-file executable. You can run PySpy from any folder location you like.

If you want to build PySpy into an executable yourself, then the pyinstaller spec file is provided, you will likely need to provide the api-ms-core dlls that python requires. details of this can be found [here](https://github.com/pyinstaller/pyinstaller/issues/4047#issuecomment-460869714). You will know you need them if pyinstaller complains about missing them when run.

## Uninstalling PySpy

Delete the PySpy executable and remove the following files manually:

* **Windows**: PySpy saves preference and log files in a folder called  `PySpy` located at `%LocalAppData%`.

## Dependencies & Acknowledgements

* PySpy is written in [Python 3](https://www.python.org/), licensed under [PSF's License Agreement](https://docs.python.org/3/license.html#psf-license-agreement-for-python-release).
* For API connectivity, PySpy relies on [Requests](http://docs.python-requests.org/), licensed under the [Apache License, Version 2.0](http://docs.python-requests.org/en/master/user/intro/#requests-license).
* Clipboard monitoring is implemented with the help of [pyperclip](https://github.com/asweigart/pyperclip), licensed under the [3-Clause BSD License](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt).
* The GUI is powered by [wxPython](https://www.wxpython.org/), licensed under the [wxWindows Library Licence](https://wxpython.org/pages/license/index.html).
* The Windows executables are built using [pyinstaller](https://www.pyinstaller.org/), licensed under [its own modified GPL license](https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt).
* PySpy's icon was created by Jojo Mendoza and is licensed under [Creative Commons (Attribution-Noncommercial 3.0 Unported)](https://creativecommons.org/licenses/by-nc/3.0/). It is available on [IconFinder](https://www.iconfinder.com/icons/1218719/cyber_hat_spy_undercover_user_icon).

## 'Virus' alerts, unsigned code

PyInstaller is frequently flagged by MS Defender and other virus scanners.  There is little I can do about this except do my best to demonstrate it is a false positive. You can see CI-built executables at https://app.circleci.com/pipelines/github/jhmartin/PySpy to see that there is no untoward code. Alternatively you can build a copy yourself.

Similarly, code signing certs for free projects are not free, so you will get an alert about that which is expected.

## License

PySpy is licensed under the [MIT](LICENSE.txt) License.

## CCP Copyright Notice

EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. CCP is in no way responsible for the content on or functioning of this website, nor can it be liable for any damage arising from the use of this website.
