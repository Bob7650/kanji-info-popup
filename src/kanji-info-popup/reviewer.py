# Copyright (C) 2026 Hubert Drążek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from aqt import gui_hooks
from aqt import mw
from aqt.qt import * 
from aqt.reviewer import Reviewer
from aqt.webview import WebContent
from typing import Any
from . import commands

def on_webview_will_set_content(web_content: WebContent, context) -> None:
    if not isinstance(context, Reviewer): return
    addon_package = mw.addonManager.addon_from_module(__name__)
    web_content.head += f"""<link rel="stylesheet" type="text/css" href="/_addons/{addon_package}/web/popover.css">
    <script type="text/javascript" src="/_addons/{addon_package}/web/popover.js" ></script>"""

def on_webview_did_recieve_js_message(callback: tuple[bool, Any],message: str, context) -> tuple[Any]:
    if not isinstance(context, Reviewer):
        return callback

    if not message.startswith("KanjiPopup"):
        return callback
    
    value = handle_command(message)

    return (True, value)

def handle_command(message: str) -> Any:
    print(f"Parsing command {message}")
    (header, data) = message.split(':',1)

    if header == "KanjiPopupContentPrep":
        return commands.make_popup_content(data)


def setup():
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    gui_hooks.webview_did_receive_js_message.append(on_webview_did_recieve_js_message)