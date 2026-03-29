from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class RangedActiveState(FighterState):
    name = "ranged_active"
    interruptible = False

    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.remaining = duration
        self.projectile_spawned = False

    def enter(self, fighter) -> None:
        fighter.set_attack_phase("ranged")
        self.remaining = self.duration
        self.projectile_spawned = False

    def update(self, fighter, dt: float) -> None:
        if not self.projectile_spawned:
            fighter.spawn_projectile()
            self.projectile_spawned = True

        self.remaining -= dt
        if self.remaining <= 0:
            fighter.state_machine.change_state(fighter.state_factory.ranged_recovery())
