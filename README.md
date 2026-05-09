# Description
This is an Anki Add-on that allows a convenient access to basic information about Japanese Kanji, without leaving Anki. It comes with data about all the Jōyō Kanji already saved so you can use if offline. Other Kanji will be automatically fetched from the API when selected, and saved for future lookup (requires access to the internet).

## This add-on can display:
- English meanings,
- native Japanese readings (kunyomi),
- Chinese readings (onyomi),
- kanji grade,
- JLPT level,
- stroke count.

Displayed data can be adjusted in Add-on settings.

# Installation
There are two ways of installing Anki Add-ons:

**From AnkiWeb (recommended):**
1. Go on the [AnkiWeb](//TODO put link here) and copy the code of this Add-on.
2. Startup your Anki and navigate to `Tools->Add-ons`.
3. Press `Get Add-ons...` and paste the code there.
4. Press "OK" and restart Anki.

**From file:**
1. Download the .ankiaddon file below
2. Startup your Anki and navigate to `Tools->Add-ons`.
3. Press `Install from file...` and choose the downloaded file
4. Restart Anki

# Usage

Select one or more kanji and the pop-up will display:

![popup image](https://github.com/Bob7650/kanji-info-popover/blob/main/screenshots/popup.png)

You can also move the popup around by dragging it by the handle on the top left:

![popup drag gif](https://github.com/Bob7650/kanji-info-popover/blob/main/screenshots/popup_drag.gif)

# Credits & Third-Party Resources

## Kanji Data
This add-on includes kanji data sourced from [KanjiAPI.dev](https://kanjiapi.dev/) (© onlyskin), which is built on the [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project) dictionary, a property of the [Electronic Dictionary Research and Development Group (EDRDG)](https://www.edrdg.org/), used in conformance with the Group's [licence](https://www.edrdg.org/edrdg/licence.html).

## The Jōyō Kanji list
The database generation script fetches the kanji list from [kanji-data](https://github.com/davidluzgouveia/kanji-data) by David Luz Gouveia.

# License
This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
