from __future__ import annotations

from tests.test_helpers import make_fighter


def test_hit_never_reduces_health_below_zero() -> None:
    fighter = make_fighter()
    fighter.health = 5

    fighter.receive_hit(999, 0.0, 0.0)

    assert fighter.health == 0


def test_ko_signal_is_returned_when_health_reaches_zero() -> None:
    fighter = make_fighter()
    fighter.health = 5

    ko = fighter.receive_hit(5, 1.0, 1.0)

    assert ko is True
    assert fighter.health == 0
    assert fighter.state_name == "hitstun"


def test_non_shooter_cannot_queue_projectile() -> None:
    fighter = make_fighter(can_shoot=False)

    assert fighter.queue_ranged() is False
    assert fighter.try_projectile() is None


def test_jump_count_resets_after_landing_update_cycle() -> None:
    fighter = make_fighter()
    fighter.jump_count = 2
    fighter.on_ground = False
    fighter.body.y = 10000

    fighter.update(0.016)

    assert fighter.on_ground is True
    assert fighter.jump_count == 0
