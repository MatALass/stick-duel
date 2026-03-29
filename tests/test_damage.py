from stick_duel.combat.damage import apply_damage


def test_apply_damage_never_goes_below_zero() -> None:
    assert apply_damage(10, 15) == 0


def test_apply_damage_reduces_health() -> None:
    assert apply_damage(100, 18) == 82
