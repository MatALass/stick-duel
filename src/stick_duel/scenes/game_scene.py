
from __future__ import annotations

import pygame

from stick_duel.combat.collision import intersects
from stick_duel.constants import BG_BOTTOM, BG_TOP, GROUND_FILL, GROUND_LINE, GROUND_Y, HEIGHT, ORANGE, SOFT_TEXT, WHITE, WIDTH
from stick_duel.core.scene import Scene, SceneResult
from stick_duel.effects.impact import HitFreeze, ImpactParticles, ScreenShake
from stick_duel.entities.fighter import Fighter
from stick_duel.ui.hud import draw_hud


class GameScene(Scene):
    def enter(self, payload: dict | None = None) -> None:
        payload = payload or {}
        fighters = payload['fighters']
        self.background = self.game.assets.optional_image('images/background/fonde.png', size=(WIDTH, HEIGHT), fill_color=BG_BOTTOM)
        self.pause_font = self.game.assets.font(42, bold=True)
        self.info_font = self.game.assets.font(20)
        self.big_font = self.game.assets.font(72, bold=True)
        self.match_over = False
        self.projectiles = []
        self.screen_shake = ScreenShake()
        self.hit_freeze = HitFreeze()
        self.impact_particles = ImpactParticles()

        self.player1 = Fighter(
            player_id=1,
            name=payload['p1_name'],
            definition=fighters[payload['p1_fighter']],
            spawn=(250, 300),
            controls={'left': pygame.K_q, 'right': pygame.K_d},
        )
        self.player2 = Fighter(
            player_id=2,
            name=payload['p2_name'],
            definition=fighters[payload['p2_fighter']],
            spawn=(1280, 300),
            controls={'left': pygame.K_LEFT, 'right': pygame.K_RIGHT},
        )
        self.players = [self.player1, self.player2]
        self.paused = False

    def handle_event(self, event: pygame.event.Event) -> SceneResult | None:
        if event.type == pygame.QUIT:
            return SceneResult(quit_game=True)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            if self.paused:
                return None
            if event.key == pygame.K_z:
                self.player1.queue_jump()
            elif event.key == pygame.K_s:
                self.player1.queue_fast_fall()
            elif event.key == pygame.K_f:
                self.player1.queue_melee()
            elif event.key == pygame.K_g:
                self.player1.queue_ranged()
            elif event.key == pygame.K_UP:
                self.player2.queue_jump()
            elif event.key == pygame.K_DOWN:
                self.player2.queue_fast_fall()
            elif event.key == pygame.K_RETURN:
                self.player2.queue_melee()
            elif event.key == pygame.K_RSHIFT:
                self.player2.queue_ranged()
        return None

    def update(self, dt: float) -> SceneResult | None:
        self.screen_shake.update(dt)
        self.hit_freeze.update(dt)
        self.impact_particles.update(dt)

        if self.paused:
            return None

        if self.hit_freeze.active:
            return None

        pressed = pygame.key.get_pressed()
        self.player1.handle_input(pressed)
        self.player2.handle_input(pressed)

        for fighter in self.players:
            fighter.update(dt)
            self.projectiles.extend(fighter.drain_spawned_projectiles())

        self._resolve_melee_hits()
        self._update_projectiles(dt)

        winner = self._check_winner()
        if winner is not None:
            return SceneResult(next_scene='victory', payload={'winner_name': winner.name, 'winner_fighter': winner.definition.display_name})
        return None

    def _trigger_hit_effects(self, x: float, y: float, color: tuple[int, int, int], strong: bool = False) -> None:
        self.hit_freeze.trigger(0.055 if strong else 0.04)
        self.screen_shake.trigger(8 if strong else 5, 0.14 if strong else 0.10)
        self.impact_particles.spawn(x, y, color=color, count=14 if strong else 10)

    def _resolve_melee_hits(self) -> None:
        if self.player1.state_name == 'melee_active' and not self.player1.melee_contact_consumed:
            if intersects(self.player1.melee_hitbox(), self.player2.rect):
                self._apply_fighter_hit(self.player2, self.player1)
                self.player1.consume_melee_contact()
        if self.player2.state_name == 'melee_active' and not self.player2.melee_contact_consumed:
            if intersects(self.player2.melee_hitbox(), self.player1.rect):
                self._apply_fighter_hit(self.player1, self.player2)
                self.player2.consume_melee_contact()

    def _apply_fighter_hit(self, target: Fighter, attacker: Fighter) -> None:
        attack = attacker.melee_attack
        hit_x = target.rect.centerx
        hit_y = target.rect.centery
        ko = target.receive_hit(attack.damage, attack.knockback_x * attacker.facing, attack.knockback_y)
        self._trigger_hit_effects(hit_x, hit_y, attacker.definition.stats.accent_color, strong=ko)
        if ko:
            target.stocks -= 1
            if target.stocks >= 0:
                spawn = (250, 300) if target.player_id == 1 else (1280, 300)
                target.reset_after_stock_loss(spawn)
            else:
                target.state_machine.change_state(target.state_factory.dead())

    def _update_projectiles(self, dt: float) -> None:
        for projectile in self.projectiles:
            projectile.update(dt, WIDTH)
            target = self.player2 if projectile.owner_id == 1 else self.player1
            if projectile.alive and intersects(projectile.rect(), target.rect):
                hit_x = target.rect.centerx
                hit_y = target.rect.centery
                ko = target.receive_hit(projectile.damage, projectile.knockback_x, projectile.knockback_y)
                projectile.alive = False
                self._trigger_hit_effects(hit_x, hit_y, projectile.color, strong=ko)
                if ko:
                    target.stocks -= 1
                    if target.stocks >= 0:
                        spawn = (250, 300) if target.player_id == 1 else (1280, 300)
                        target.reset_after_stock_loss(spawn)
                    else:
                        target.state_machine.change_state(target.state_factory.dead())
        self.projectiles = [p for p in self.projectiles if p.alive]

    def _check_winner(self) -> Fighter | None:
        if self.player1.stocks < 0:
            return self.player2
        if self.player2.stocks < 0:
            return self.player1
        return None

    def draw(self, screen: pygame.Surface) -> None:
        world = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        world.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 68))
        world.blit(overlay, (0, 0))
        gradient = self.game.assets.build_vertical_gradient((WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)
        gradient.set_alpha(30)
        world.blit(gradient, (0, 0))

        pygame.draw.rect(world, GROUND_FILL, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.line(world, GROUND_LINE, (0, GROUND_Y), (WIDTH, GROUND_Y), 4)

        for projectile in self.projectiles:
            projectile.draw(world)

        offset = self.screen_shake.get_offset()
        self.player1.draw(world, offset)
        self.player2.draw(world, offset)
        self.impact_particles.draw(world, offset)

        screen.fill((0, 0, 0))
        screen.blit(world, offset)
        draw_hud(screen, self.game.assets, self.player1, self.player2)

        hint = self.info_font.render('Blue  Q D Z S F G   •   Red  Arrows Enter Right Shift', True, SOFT_TEXT)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 32)))

        if self.paused:
            panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 170))
            screen.blit(panel, (0, 0))
            paused = self.big_font.render('Paused', True, WHITE)
            info = self.pause_font.render('Press Esc to resume', True, ORANGE)
            screen.blit(paused, paused.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
