from aqt import mw

from . import reviewer

mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
reviewer.hook_to_anki()
