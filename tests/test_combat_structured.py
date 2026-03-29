from __future__ import annotations

from tests.test_helpers import make_fighter


def test_melee_attack_enters_active_phase_and_forces_recovery_after_contact() -> None:
    fighter = make_fighter(can_shoot=False)
    fighter.on_ground = True

    assert fighter.queue_melee() is True

    fighter.update(0.01)
    assert fighter.state_name == "melee_startup"

    fighter.update(0.09)
    assert fighter.state_name == "melee_active"

    fighter.consume_melee_contact()
    assert fighter.state_name == "melee_recovery"


def test_projectile_attack_spawns_exactly_one_projectile_after_startup() -> None:
    fighter = make_fighter(can_shoot=True)
    queued = fighter.try_projectile()

    assert queued is not None

    fighter.update(0.016)
    fighter.update(0.06)
    fighter.update(0.04)

    projectiles = fighter.drain_spawned_projectiles()

    assert len(projectiles) == 1
    assert projectiles[0].alive is True
    assert projectiles[0].owner_id == fighter.player_id
    assert projectiles[0].damage == fighter.definition.stats.projectile_damage
