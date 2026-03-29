from stick_duel.entities.fighter import Fighter, FighterDefinition
from stick_duel.entities.stats import FighterStats


def _definition(can_shoot: bool) -> FighterDefinition:
    return FighterDefinition(
        key="test",
        display_name="Test",
        description="Test fighter",
        stats=FighterStats(
            max_health=100,
            move_speed=8.0,
            jump_strength=15.0,
            melee_damage=10,
            melee_range=(80, 60),
            melee_knockback=(8.0, 9.0),
            melee_cooldown=0.5,
            projectile_damage=12,
            projectile_speed=450.0,
            projectile_cooldown=0.8,
            projectile_knockback=(6.0, 7.0),
            color=(255, 255, 255),
            accent_color=(255, 0, 0),
        ),
        can_shoot=can_shoot,
    )


def test_fighter_jump_increments_jump_count() -> None:
    fighter = Fighter(1, "P1", _definition(False), (0, 400), {"left": 0, "right": 0})
    fighter.jump()
    fighter.update(0.016)
    assert fighter.jump_count == 1
    assert fighter.body.velocity_y < 0


def test_ranged_attack_returns_none_for_non_shooter() -> None:
    fighter = Fighter(1, "P1", _definition(False), (0, 400), {"left": 0, "right": 0})
    assert fighter.try_projectile() is None


def test_ranged_attack_spawns_projectile_for_shooter_after_state_progression() -> None:
    fighter = Fighter(1, "P1", _definition(True), (0, 400), {"left": 0, "right": 0})
    queued = fighter.try_projectile()
    assert queued is not None

    fighter.update(0.016)
    fighter.update(0.06)
    fighter.update(0.04)

    projectiles = fighter.drain_spawned_projectiles()
    assert len(projectiles) == 1
    assert projectiles[0].damage == 12
    assert fighter.state_name in {"ranged_active", "ranged_recovery"}
