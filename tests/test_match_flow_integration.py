from __future__ import annotations

from stick_duel.entities.fighter import FighterDefinition
from stick_duel.entities.stats import FighterStats
from stick_duel.scenes.game_scene import GameScene
from tests.test_helpers import DummyGame


def make_fighters_catalog() -> dict[str, FighterDefinition]:
    swordsman = FighterDefinition(
        key="swordsman",
        display_name="Swordsman",
        description="Close-range fighter",
        stats=FighterStats(
            max_health=100,
            move_speed=8.0,
            jump_strength=15.0,
            melee_damage=20,
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
            melee_damage=10,
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


def build_scene() -> GameScene:
    scene = GameScene(DummyGame())
    scene.enter(
        {
            "p1_name": "Alice",
            "p2_name": "Bob",
            "p1_fighter": "archer",
            "p2_fighter": "swordsman",
            "fighters": make_fighters_catalog(),
        }
    )
    return scene


def test_projectile_ko_with_remaining_stock_triggers_respawn_instead_of_victory() -> None:
    scene = build_scene()
    attacker = scene.player1
    target = scene.player2

    target.stocks = 1
    target.health = attacker.definition.stats.projectile_damage
    target.body.x = 330
    target.body.y = attacker.body.y

    assert attacker.queue_ranged() is True

    result = None
    for dt in (0.016, 0.06, 0.04):
        result = scene.update(dt)

    assert result is None
    assert target.stocks == 0
    assert target.state_name in {"dead", "respawn"}


def test_final_projectile_ko_returns_victory_scene_result() -> None:
    scene = build_scene()
    attacker = scene.player1
    target = scene.player2

    target.stocks = 0
    target.health = attacker.definition.stats.projectile_damage
    target.body.x = 330
    target.body.y = attacker.body.y

    assert attacker.queue_ranged() is True

    result = None
    for dt in (0.016, 0.06, 0.04):
        result = scene.update(dt)

    assert result is not None
    assert result.next_scene == "victory"
    assert result.payload["winner_name"] == attacker.name
    assert result.payload["winner_fighter"] == attacker.definition.display_name


def test_melee_contact_reduces_health_and_consumes_attack_contact_once() -> None:
    scene = build_scene()
    attacker = scene.player1
    target = scene.player2

    attacker.body.x = 260
    attacker.body.y = 300
    target.body.x = attacker.rect.right - 15
    target.body.y = attacker.body.y
    attacker.on_ground = True

    starting_health = target.health

    assert attacker.queue_melee() is True

    attacker.update(0.01)
    attacker.update(0.09)
    scene._resolve_melee_hits()

    first_hit_health = target.health

    assert first_hit_health == starting_health - attacker.melee_attack.damage
    assert attacker.melee_contact_consumed is True

    scene._resolve_melee_hits()

    assert target.health == first_hit_health