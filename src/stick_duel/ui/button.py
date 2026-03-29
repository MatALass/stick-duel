import pygame


class Button:
    def __init__(self, rect, text, color, hover_color, text_color):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def clicked(self, event):
        # 🔥 FIX : uniquement sur clic souris gauche
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen, font, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        text_surface = font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.center),
        )