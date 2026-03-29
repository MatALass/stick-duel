from stick_duel.entities.fighter import Fighter, FighterDefinition
from stick_duel.entities.stats import FighterStats


def _definition(can_shoot: bool = True) -> FighterDefinition:
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


def test_melee_state_flow_progresses_through_attack_phases() -> None:
    fighter = Fighter(1, "P1", _definition(False), (0, 400), {"left": 0, "right": 0})
    fighter.on_ground = True

    assert fighter.queue_melee() is True
    fighter.update(0.01)
    assert fighter.state_name == "melee_startup"

    fighter.update(0.09)
    assert fighter.state_name == "melee_active"

    fighter.consume_melee_contact()
    assert fighter.state_name == "melee_recovery"


def test_receive_hit_enters_hitstun() -> None:
    fighter = Fighter(1, "P1", _definition(), (0, 400), {"left": 0, "right": 0})
    fighter.receive_hit(10, 5.0, 6.0)
    assert fighter.state_name == "hitstun"
