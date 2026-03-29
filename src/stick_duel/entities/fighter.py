from __future__ import annotations

import math

import pygame

from stick_duel.combat.attack_data import AttackData
from stick_duel.combat.attacks import Projectile
from stick_duel.combat.damage import apply_damage
from stick_duel.config import ASSETS_DIR
from stick_duel.constants import DEFAULT_STOCKS, FAST_FALL, GROUND_Y, WHITE
from stick_duel.core.state_machine import StateMachine
from stick_duel.core.timer import Cooldown
from stick_duel.entities.animation import Animation
from stick_duel.entities.fighter_input import FighterInput
from stick_duel.entities.physics import PhysicsBody
from stick_duel.entities.state_factory import FighterStateFactory
from stick_duel.entities.stats import FighterStats


class FighterDefinition:
    def __init__(self, key: str, display_name: str, description: str, stats: FighterStats, can_shoot: bool) -> None:
        self.key = key
        self.display_name = display_name
        self.description = description
        self.stats = stats
        self.can_shoot = can_shoot


class Fighter:
    def __init__(
        self,
        player_id: int,
        name: str,
        definition: FighterDefinition,
        spawn: tuple[int, int],
        controls: dict[str, int | tuple[int, ...]],
    ) -> None:
        self.player_id = player_id
        self.name = name
        self.definition = definition
        self.controls = controls
        self.spawn = spawn

        self.body = PhysicsBody(x=spawn[0], y=spawn[1], width=70, height=120)
        self.facing = 1 if player_id == 1 else -1
        self.health = definition.stats.max_health
        self.stocks = DEFAULT_STOCKS
        self.on_ground = False
        self.jump_count = 0
        self.flash_timer = 0.0
        self.respawn_invulnerability_timer = 0.0

        self.melee_cooldown = Cooldown(definition.stats.melee_cooldown)
        self.projectile_cooldown = Cooldown(definition.stats.projectile_cooldown)
        self.hitstun_duration = 0.18

        self.input_state = FighterInput()
        self.spawned_projectiles: list[Projectile] = []
        self.is_attacking = False
        self.attack_kind = 'idle'
        self.melee_contact_consumed = False

        range_x, range_y = definition.stats.melee_range
        knockback_x, knockback_y = definition.stats.melee_knockback
        self.melee_attack = AttackData(
            name='melee',
            startup=0.08,
            active=0.10,
            recovery=0.16,
            damage=definition.stats.melee_damage,
            knockback_x=knockback_x,
            knockback_y=knockback_y,
            hitbox_width=range_x,
            hitbox_height=range_y,
            hitbox_offset_x=4,
            hitbox_offset_y=0,
        )
        self.ranged_attack = AttackData(
            name='ranged',
            startup=0.05,
            active=0.03,
            recovery=0.22,
            damage=definition.stats.projectile_damage,
            knockback_x=definition.stats.projectile_knockback[0],
            knockback_y=definition.stats.projectile_knockback[1],
            hitbox_width=0,
            hitbox_height=0,
            hitbox_offset_x=0,
            hitbox_offset_y=0,
        )

        self.animation = self._load_animation()
        self.state_factory = FighterStateFactory(self)
        self.state_machine = StateMachine(self, self.state_factory.idle())

    def _load_animation(self) -> Animation | None:
        image_path = ASSETS_DIR / 'images/fighters/spritesheet.png'
        if not image_path.exists():
            return None
        if not pygame.get_init() or pygame.display.get_surface() is None:
            return None
        try:
            animation = Animation(str(image_path), 64, 64, speed=0.10)
            animation.add_animation('idle', 0, 1)
            animation.add_animation('run', 1, 8)
            animation.add_animation('attack', 3, 1)
            return animation
        except Exception:
            return None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.body.x), int(self.body.y), self.body.width, self.body.height)

    @property
    def state_name(self) -> str:
        return self.state_machine.state_name

    def set_attack_phase(self, phase: str) -> None:
        self.attack_kind = phase
        self.is_attacking = phase in {'melee', 'melee_recovery', 'ranged', 'ranged_recovery'}

    def reset_after_stock_loss(self, spawn: tuple[int, int]) -> None:
        self.spawn = spawn
        self.body.x = spawn[0]
        self.body.y = spawn[1]
        self.body.velocity_x = 0.0
        self.body.velocity_y = 0.0
        self.health = self.definition.stats.max_health
        self.jump_count = 0
        self.on_ground = False
        self.flash_timer = 0.6
        self.respawn_invulnerability_timer = 0.5
        self.set_attack_phase('idle')
        self.melee_contact_consumed = False
        self.state_machine.change_state(self.state_factory.respawn())

    def set_pressed_input(self, pressed: pygame.key.ScancodeWrapper) -> None:
        self.input_state.left = bool(pressed[self.controls['left']])
        self.input_state.right = bool(pressed[self.controls['right']])

    def handle_input(self, pressed: pygame.key.ScancodeWrapper) -> list[Projectile]:
        self.set_pressed_input(pressed)
        return []

    def has_horizontal_input(self) -> bool:
        return self.input_state.left ^ self.input_state.right

    def apply_horizontal_input(self, acceleration: float) -> None:
        boost = max(0.65, self.definition.stats.move_speed / 8.0)
        effective_acceleration = acceleration * boost
        if self.input_state.left and not self.input_state.right:
            self.body.velocity_x -= effective_acceleration
            self.facing = -1
        elif self.input_state.right and not self.input_state.left:
            self.body.velocity_x += effective_acceleration
            self.facing = 1

    def queue_jump(self) -> None:
        self.input_state.jump_pressed = True

    def queue_fast_fall(self) -> None:
        self.input_state.fast_fall_pressed = True

    def queue_melee(self) -> bool:
        if not self.can_start_melee():
            return False
        self.input_state.melee_pressed = True
        return True

    def queue_ranged(self) -> bool:
        if not self.can_start_ranged():
            return False
        self.input_state.ranged_pressed = True
        return True

    def try_consume_jump_input(self) -> bool:
        return self.input_state.consume_jump()

    def try_consume_fast_fall_input(self) -> bool:
        return self.input_state.consume_fast_fall()

    def try_consume_melee_input(self) -> bool:
        return self.input_state.consume_melee()

    def try_consume_ranged_input(self) -> bool:
        return self.input_state.consume_ranged()

    def can_start_melee(self) -> bool:
        blocked_states = {
            'melee_startup', 'melee_active', 'melee_recovery',
            'ranged_startup', 'ranged_active', 'ranged_recovery',
            'hitstun', 'dead', 'respawn',
        }
        return self.melee_cooldown.ready() and self.state_name not in blocked_states

    def can_start_ranged(self) -> bool:
        blocked_states = {
            'melee_startup', 'melee_active', 'melee_recovery',
            'ranged_startup', 'ranged_active', 'ranged_recovery',
            'hitstun', 'dead', 'respawn',
        }
        return self.definition.can_shoot and self.projectile_cooldown.ready() and self.state_name not in blocked_states

    def start_melee_sequence(self) -> None:
        self.melee_cooldown.trigger()
        self.state_machine.change_state(self.state_factory.melee_startup())

    def start_ranged_sequence(self) -> None:
        self.projectile_cooldown.trigger()
        self.state_machine.change_state(self.state_factory.ranged_startup())

    def jump(self) -> None:
        self.queue_jump()

    def perform_jump(self) -> None:
        if self.jump_count < 2:
            self.body.velocity_y = -self.definition.stats.jump_strength
            self.jump_count += 1
            self.on_ground = False

    def fast_fall(self) -> None:
        if not self.on_ground:
            self.body.velocity_y += FAST_FALL

    def melee_hitbox(self) -> pygame.Rect:
        attack = self.melee_attack
        width = attack.hitbox_width
        height = attack.hitbox_height
        top = self.rect.centery - height // 2 + attack.hitbox_offset_y
        if self.facing == 1:
            left = self.rect.right + attack.hitbox_offset_x
        else:
            left = self.rect.left - width - attack.hitbox_offset_x
        return pygame.Rect(left, top, width, height)

    def try_melee(self) -> bool:
        return self.queue_melee()

    def try_projectile(self) -> Projectile | None:
        queued = self.queue_ranged()
        if queued:
            return Projectile(owner_id=self.player_id, x=0, y=0, vx=0, damage=self.definition.stats.projectile_damage, knockback_x=0, knockback_y=0, color=self.definition.stats.accent_color, radius=7, alive=False, kind='arrow')
        return None

    def spawn_projectile(self) -> None:
        if not self.definition.can_shoot:
            return
        speed = self.definition.stats.projectile_speed * self.facing
        projectile = Projectile(
            owner_id=self.player_id,
            x=self.rect.centerx + (40 * self.facing),
            y=self.rect.centery - 10,
            vx=speed,
            damage=self.definition.stats.projectile_damage,
            knockback_x=self.definition.stats.projectile_knockback[0] * self.facing,
            knockback_y=self.definition.stats.projectile_knockback[1],
            color=self.definition.stats.accent_color,
            radius=7,
            kind='arrow',
        )
        self.spawned_projectiles.append(projectile)

    def drain_spawned_projectiles(self) -> list[Projectile]:
        projectiles = list(self.spawned_projectiles)
        self.spawned_projectiles.clear()
        return projectiles

    def consume_melee_contact(self) -> None:
        self.melee_contact_consumed = True
        if self.state_name == 'melee_active':
            self.state_machine.change_state(self.state_factory.melee_recovery())

    def receive_hit(self, damage: int, knockback_x: float, knockback_y: float) -> bool:
        if self.respawn_invulnerability_timer > 0:
            return False
        self.health = apply_damage(self.health, damage)
        self.body.velocity_x += knockback_x
        self.body.velocity_y = -abs(knockback_y)
        self.flash_timer = 0.14
        self.set_attack_phase('idle')
        self.melee_contact_consumed = True
        self.state_machine.change_state(self.state_factory.hitstun())
        return self.health <= 0

    def update(self, dt: float) -> None:
        self.melee_cooldown.update(dt)
        self.projectile_cooldown.update(dt)
        self.flash_timer = max(0.0, self.flash_timer - dt)
        self.respawn_invulnerability_timer = max(0.0, self.respawn_invulnerability_timer - dt)

        self.state_machine.update(dt)

        self.body.apply_gravity()
        self.body.apply_friction()
        self.body.clamp_velocity()
        self.body.step()

        previous_on_ground = self.on_ground
        if self.body.y + self.body.height >= GROUND_Y:
            self.body.y = GROUND_Y - self.body.height
            self.body.velocity_y = 0.0
            self.on_ground = True
            if not previous_on_ground:
                self.jump_count = 0
        else:
            self.on_ground = False

        self._sync_animation_name()
        if self.animation is not None:
            self.animation.update(dt)

    def _sync_animation_name(self) -> None:
        if self.animation is None:
            return
        if self.state_name in {'melee_startup', 'melee_active', 'melee_recovery', 'ranged_startup', 'ranged_active', 'ranged_recovery'}:
            self.animation.set_animation('attack')
        elif self.state_name == 'run':
            self.animation.set_animation('run')
        else:
            self.animation.set_animation('idle')

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        if self.animation is not None:
            self._draw_sprite(screen, offset)
        else:
            self._draw_placeholder(screen, offset)

    def _current_body_color(self) -> tuple[int, int, int]:
        if self.respawn_invulnerability_timer > 0 and int(self.respawn_invulnerability_timer * 18) % 2 == 0:
            return (255, 255, 255)
        if self.flash_timer > 0 and int(self.flash_timer * 20) % 2 == 0:
            return (255, 255, 255)
        return self.definition.stats.color

    def _draw_sprite(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        ox, oy = offset
        frame_rect = self.animation.get_current_frame()
        raw = self.animation.sheet.subsurface(frame_rect).copy()
        # Crop more aggressively to avoid stray pixels from neighboring frames.
        cropped = raw.subsurface(pygame.Rect(6, 6, 52, 52)).copy()
        sprite = pygame.Surface(cropped.get_size(), pygame.SRCALPHA)
        body_color = self._current_body_color()
        accent = self.definition.stats.accent_color

        width, height = cropped.get_size()
        for x in range(width):
            for y in range(height):
                r, g, b, a = cropped.get_at((x, y))
                if a == 0 or (r > 232 and g > 232 and b > 232):
                    sprite.set_at((x, y), (0, 0, 0, 0))
                elif r > 160 and g < 130 and b < 130:
                    sprite.set_at((x, y), (*accent, 255))
                else:
                    sprite.set_at((x, y), (*body_color, 255))

        glow = pygame.Surface((140, 140), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*accent, 34), (70, 70), 44)
        screen.blit(glow, (self.rect.centerx + ox - 70, self.rect.bottom + oy - 122))

        shadow = pygame.Surface((100, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 90 if self.on_ground else 45), shadow.get_rect())
        screen.blit(shadow, (self.rect.centerx + ox - 50, self.rect.bottom + oy - 10))

        sprite = pygame.transform.scale(sprite, (112, 112))
        if self.facing == -1:
            sprite = pygame.transform.flip(sprite, True, False)
        dest = sprite.get_rect(midbottom=(self.rect.centerx + ox, self.rect.bottom + oy + 2))
        screen.blit(sprite, dest)

        if self.definition.can_shoot and self.state_name in {'ranged_startup', 'ranged_active', 'ranged_recovery'}:
            bow_x = self.rect.centerx + ox + 18 * self.facing
            top = self.rect.top + oy
            bow_rect = pygame.Rect(bow_x - 10, top + 28, 22, 46)
            if self.facing == 1:
                pygame.draw.arc(screen, accent, bow_rect, 0.9, 5.2, 3)
            else:
                pygame.draw.arc(screen, accent, bow_rect, 4.3, 2.0, 3)
            pygame.draw.line(screen, accent, (bow_x, top + 30), (bow_x, top + 70), 2)
            pygame.draw.line(screen, (255, 255, 255), (bow_x, top + 50), (bow_x + 24 * self.facing, top + 50), 2)

    def _draw_placeholder(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        ox, oy = offset
        t = pygame.time.get_ticks() / 1000.0
        accent = self.definition.stats.accent_color
        body_color = self._current_body_color()

        x = self.rect.centerx + ox
        y = self.rect.bottom + oy
        swing = math.sin(t * 9.0) * 12 if self.state_name == 'run' and self.on_ground else 0
        bob = math.sin(t * 4.2) * 2 if self.on_ground and self.state_name in {'idle', 'run'} else 0

        head_y = y - 98 + bob
        torso_top = y - 76 + bob
        torso_bottom = y - 28 + bob
        shadow = pygame.Surface((120, 40), pygame.SRCALPHA)
        shadow_alpha = 70 if self.on_ground else 35
        pygame.draw.ellipse(shadow, (0, 0, 0, shadow_alpha), shadow.get_rect())
        screen.blit(shadow, (x - 60, y - 14))

        glow = pygame.Surface((140, 140), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*accent, 30), (70, 70), 44)
        screen.blit(glow, (x - 70, y - 122))

        pygame.draw.circle(screen, body_color, (int(x), int(head_y)), 17, 3)
        pygame.draw.line(screen, body_color, (int(x), int(torso_top)), (int(x), int(torso_bottom)), 4)

        arm_y = torso_top + 22
        if self.state_name in {'melee_startup', 'melee_active', 'melee_recovery'}:
            front_arm_end = (x + 30 * self.facing, arm_y - 8)
            back_arm_end = (x - 18 * self.facing, arm_y + 16)
        elif self.state_name in {'ranged_startup', 'ranged_active', 'ranged_recovery'}:
            front_arm_end = (x + 26 * self.facing, arm_y)
            back_arm_end = (x - 16 * self.facing, arm_y - 6)
        else:
            front_arm_end = (x + 24 * self.facing, arm_y + swing * 0.35)
            back_arm_end = (x - 24 * self.facing, arm_y - swing * 0.35)

        pygame.draw.line(screen, body_color, (int(x), int(arm_y)), (int(front_arm_end[0]), int(front_arm_end[1])), 4)
        pygame.draw.line(screen, body_color, (int(x), int(arm_y)), (int(back_arm_end[0]), int(back_arm_end[1])), 4)
        pygame.draw.line(screen, body_color, (int(x), int(torso_bottom)), (int(x - 16), int(y)), 4)
        pygame.draw.line(screen, body_color, (int(x), int(torso_bottom)), (int(x + 16), int(y)), 4)

        if self.state_name in {'melee_startup', 'melee_active', 'melee_recovery'}:
            tip = (int(front_arm_end[0] + 18 * self.facing), int(front_arm_end[1] - 18))
            pygame.draw.line(screen, accent, (int(front_arm_end[0]), int(front_arm_end[1])), tip, 5)
            pygame.draw.circle(screen, accent, tip, 5)
        if self.definition.can_shoot and self.state_name in {'ranged_startup', 'ranged_active', 'ranged_recovery'}:
            bow_x = int(front_arm_end[0])
            bow_y = int(front_arm_end[1])
            bow_rect = pygame.Rect(bow_x - 10, bow_y - 18, 20, 36)
            if self.facing == 1:
                pygame.draw.arc(screen, accent, bow_rect, 0.9, 5.2, 3)
            else:
                pygame.draw.arc(screen, accent, bow_rect, 4.3, 2.0, 3)
            pygame.draw.line(screen, accent, (bow_x, bow_y - 18), (bow_x, bow_y + 18), 2)
            pygame.draw.line(screen, WHITE, (bow_x, bow_y), (bow_x + 18 * self.facing, bow_y), 2)
