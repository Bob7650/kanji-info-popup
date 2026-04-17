import aqt
from aqt import mw
from . import reviewer
from .qt import ConfigWindow

mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
# register config and deck cache windows
# aqt.DialogManager.register_dialog("KIPConfigWindow", [ConfigWindow, None])
reviewer.setup()

