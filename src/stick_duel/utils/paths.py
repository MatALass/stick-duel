from __future__ import annotations

from pathlib import Path


def safe_path(*parts: str) -> Path:
    return Path(*parts).resolve()
