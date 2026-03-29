from __future__ import annotations

from stick_duel.core.scene import SceneResult
from stick_duel.entities.fighter import FighterDefinition
from stick_duel.entities.stats import FighterStats
from stick_duel.scenes.game_scene import GameScene
from tests.test_helpers import DummyGame


def build_game_scene() -> GameScene:
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


def test_melee_contact_in_game_scene_deals_damage_and_forces_recovery() -> None:
    scene = build_game_scene()
    attacker = scene.player1
    target = scene.player2

    target.body.x = attacker.rect.right + 10
    target.body.y = attacker.body.y
    attacker.on_ground = True

    assert attacker.queue_melee() is True

    attacker.update(0.01)
    attacker.update(0.09)
    starting_health = target.health

    scene._resolve_melee_hits()

    assert target.health == starting_health - attacker.melee_attack.damage
    assert target.state_name == "hitstun"
    assert attacker.melee_contact_consumed is True
    assert attacker.state_name == "melee_recovery"


def test_projectile_hit_on_last_stock_sets_dead_state_and_winner() -> None:
    scene = build_game_scene()
    attacker = scene.player1
    target = scene.player2

    target.stocks = 0
    target.health = attacker.definition.stats.projectile_damage
    target.body.x = 330
    target.body.y = attacker.body.y

    assert attacker.queue_ranged() is True

    attacker.update(0.016)
    attacker.update(0.06)
    attacker.update(0.04)
    scene.projectiles.extend(attacker.drain_spawned_projectiles())

    scene._update_projectiles(0.016)

    assert scene.projectiles == []
    assert target.stocks == -1
    assert target.state_name == "dead"
    assert scene._check_winner() is attacker


def test_update_returns_victory_scene_result_after_final_projectile_ko() -> None:
    scene = build_game_scene()
    attacker = scene.player1
    target = scene.player2

    target.stocks = 0
    target.health = attacker.definition.stats.projectile_damage
    target.body.x = 330
    target.body.y = attacker.body.y

    assert attacker.queue_ranged() is True

    result: SceneResult | None = None
    for dt in (0.016, 0.06, 0.04):
        result = scene.update(dt)

    assert result is not None
    assert result.next_scene == "victory"
    assert result.payload["winner_name"] == attacker.name
    assert result.payload["winner_fighter"] == attacker.definition.display_name