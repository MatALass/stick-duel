from __future__ import annotations

from pathlib import Path

import pygame

from stick_duel.config import ASSETS_DIR
from stick_duel.constants import HEIGHT, LIGHT_BG, WHITE, WIDTH


class AssetLoader:
    def __init__(self) -> None:
        self.assets_dir = ASSETS_DIR
        self._font_cache: dict[tuple[int, bool], pygame.font.Font] = {}
        self._image_cache: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}

    def font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._font_cache:
            self._font_cache[key] = pygame.font.SysFont("arial", size, bold=bold)
        return self._font_cache[key]

    def image(self, relative_path: str, size: tuple[int, int] | None = None, alpha: bool = True) -> pygame.Surface:
        key = (relative_path, size)
        if key in self._image_cache:
            return self._image_cache[key]

        path = self.assets_dir / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Asset not found: {path}")

        image = pygame.image.load(path.as_posix())
        image = image.convert_alpha() if alpha else image.convert()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        self._image_cache[key] = image
        return image

    def optional_image(
        self,
        relative_path: str,
        size: tuple[int, int] | None = None,
        fill_color: tuple[int, int, int] = LIGHT_BG,
    ) -> pygame.Surface:
        try:
            return self.image(relative_path, size=size)
        except FileNotFoundError:
            fallback_size = size or (WIDTH, HEIGHT)
            surface = pygame.Surface(fallback_size)
            surface.fill(fill_color)
            return surface

    def maybe_play_music(self, relative_path: str, volume: float = 0.35) -> None:
        path = self.assets_dir / relative_path
        if not path.exists():
            return
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(path.as_posix())
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def stop_music(self) -> None:
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except pygame.error:
            pass

    def build_vertical_gradient(self, size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> pygame.Surface:
        width, height = size
        surface = pygame.Surface((width, height))
        for y in range(height):
            ratio = y / max(1, height - 1)
            color = (
                int(top[0] * (1 - ratio) + bottom[0] * ratio),
                int(top[1] * (1 - ratio) + bottom[1] * ratio),
                int(top[2] * (1 - ratio) + bottom[2] * ratio),
            )
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    def outlined_text(
        self,
        text: str,
        size: int,
        color: tuple[int, int, int] = WHITE,
        outline: tuple[int, int, int] = (0, 0, 0),
        bold: bool = True,
    ) -> pygame.Surface:
        font = self.font(size, bold=bold)
        base = font.render(text, True, color)
        outlined = pygame.Surface((base.get_width() + 4, base.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in ((0, 0), (2, 0), (0, 2), (2, 2)):
            outlined.blit(font.render(text, True, outline), (dx, dy))
        outlined.blit(base, (1, 1))
        return outlined
