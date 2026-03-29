from __future__ import annotations

from pathlib import Path

from stick_duel.constants import DEFAULT_STOCKS, FPS, GROUND_Y, HEIGHT, WIDTH

ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
TARGET_FPS = FPS
GROUND_LEVEL = GROUND_Y
INITIAL_STOCKS = DEFAULT_STOCKS
