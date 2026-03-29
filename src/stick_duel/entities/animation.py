import pygame


class Animation:
    def __init__(self, image_path: str, frame_width: int, frame_height: int, speed: float = 0.15):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.speed = speed

        self.animations: dict[str, list[pygame.Rect]] = {}
        self.current_animation = ""
        self.frame_index = 0
        self.timer = 0.0

    def add_animation(self, name: str, row: int, frame_count: int) -> None:
        frames: list[pygame.Rect] = []
        for i in range(frame_count):
            rect = pygame.Rect(
                i * self.frame_width,
                row * self.frame_height,
                self.frame_width,
                self.frame_height,
            )
            frames.append(rect)

        self.animations[name] = frames

        if not self.current_animation:
            self.current_animation = name

    def set_animation(self, name: str) -> None:
        if name not in self.animations:
            raise ValueError(f"Animation '{name}' is not defined.")

        if name != self.current_animation:
            self.current_animation = name
            self.frame_index = 0
            self.timer = 0.0

    def update(self, dt: float) -> None:
        if not self.current_animation:
            return

        frames = self.animations.get(self.current_animation)
        if not frames:
            return

        self.timer += dt
        while self.timer >= self.speed:
            self.timer -= self.speed
            self.frame_index = (self.frame_index + 1) % len(frames)

    def get_current_frame(self) -> pygame.Rect:
        if not self.current_animation:
            raise ValueError("No current animation is set.")

        frames = self.animations.get(self.current_animation)
        if not frames:
            raise ValueError(f"No frames found for animation '{self.current_animation}'.")

        return frames[self.frame_index]