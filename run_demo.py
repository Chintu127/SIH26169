from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.ui.game_window import launch_game


if __name__ == "__main__":
    launch_game("clean")
