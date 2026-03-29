from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlayerSelection:
    name: str
    fighter_key: str


@dataclass
class MatchState:
    paused: bool = False
