from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class InputBox:
    rect: pygame.Rect
    text: str = ""
    active: bool = False
    placeholder: str = ""
    max_length: int = 12

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode

    def value(self) -> str:
        return self.text.strip() or self.placeholder

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, label_font: pygame.font.Font, label: str) -> None:
        panel = pygame.Rect(self.rect)
        border_color = (255, 196, 87) if self.active else (118, 136, 169)
        shadow = panel.move(0, 4)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=16)
        pygame.draw.rect(screen, (16, 23, 35), panel, border_radius=16)
        pygame.draw.rect(screen, border_color, panel, width=3, border_radius=16)
        label_surface = label_font.render(label, True, (238, 242, 249))
        screen.blit(label_surface, (panel.x + 2, panel.y - 34))
        shown_text = self.text if self.text else self.placeholder
        color = (245, 247, 250) if self.text else (160, 170, 190)
        text_surface = font.render(shown_text, True, color)
        screen.blit(text_surface, (panel.x + 16, panel.y + 14))
