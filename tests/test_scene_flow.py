from __future__ import annotations

import pygame

from stick_duel.core.scene import SceneResult
from stick_duel.core.scene_manager import SceneManager
from stick_duel.entities.fighter import FighterDefinition
from stick_duel.entities.stats import FighterStats
from stick_duel.scenes.controls_scene import ControlsScene
from stick_duel.scenes.game_scene import GameScene
from stick_duel.scenes.menu_scene import MenuScene
from stick_duel.scenes.player_setup_scene import PlayerSetupScene
from stick_duel.scenes.victory_scene import VictoryScene

from tests.test_helpers import DummyGame


def build_manager() -> SceneManager:
    game = DummyGame()
    manager = SceneManager(game)
    manager.register("menu", MenuScene)
    manager.register("controls", ControlsScene)
    manager.register("setup", PlayerSetupScene)
    manager.register("game", GameScene)
    manager.register("victory", VictoryScene)
    return manager


def make_fighters_catalog() -> dict[str, FighterDefinition]:
    swordsman = FighterDefinition(
        key="swordsman",
        display_name="Swordsman",
        description="Close-range fighter",
        stats=FighterStats(
            max_health=100,
            move_speed=8.0,
            jump_strength=15.0,
            melee_damage=12,
            melee_range=(90, 60),
            melee_knockback=(9.0, 10.0),
            melee_cooldown=0.5,
            projectile_damage=0,
            projectile_speed=0.0,
            projectile_cooldown=0.0,
            projectile_knockback=(0.0, 0.0),
            color=(255, 255, 255),
            accent_color=(255, 140, 0),
        ),
        can_shoot=False,
    )

    archer = FighterDefinition(
        key="archer",
        display_name="Archer",
        description="Ranged fighter",
        stats=FighterStats(
            max_health=100,
            move_speed=8.0,
            jump_strength=15.0,
            melee_damage=8,
            melee_range=(80, 50),
            melee_knockback=(7.0, 8.0),
            melee_cooldown=0.5,
            projectile_damage=10,
            projectile_speed=450.0,
            projectile_cooldown=0.8,
            projectile_knockback=(6.0, 7.0),
            color=(255, 255, 255),
            accent_color=(200, 60, 60),
        ),
        can_shoot=True,
    )

    return {
        "swordsman": swordsman,
        "archer": archer,
    }


def test_scene_manager_can_follow_full_happy_path() -> None:
    manager = build_manager()

    manager.go_to("menu")
    assert manager.current_name == "menu"

    manager.go_to("setup")
    assert manager.current_name == "setup"

    fighters = make_fighters_catalog()

    manager.go_to(
        "game",
        {
            "p1_name": "Alice",
            "p2_name": "Bob",
            "p1_fighter": "swordsman",
            "p2_fighter": "archer",
            "fighters": fighters,
        },
    )
    assert manager.current_name == "game"

    manager.go_to(
        "victory",
        {"winner_name": "Alice", "winner_fighter": "Swordsman"},
    )
    assert manager.current_name == "victory"

    pygame.quit()


def test_menu_scene_contract_is_explicit() -> None:
    result = SceneResult(next_scene="setup")
    assert result.next_scene == "setup"
    assert result.quit_game is False