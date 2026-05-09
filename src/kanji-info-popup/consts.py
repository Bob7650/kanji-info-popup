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

import os

CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "user_files/cache/kanji_cache.db")
USER_CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "user_files/cache/kanji_user_cache.db")
COLUMNS = ["kanji", "meanings", "on_readings", "kun_readings", "heisig_en", "grade", "jlpt", "stroke_count"]
KANJI_API = "https://kanjiapi.dev/v1/kanji/"