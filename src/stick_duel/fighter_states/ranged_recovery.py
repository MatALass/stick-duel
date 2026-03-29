from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class RangedRecoveryState(FighterState):
    name = "ranged_recovery"
    interruptible = False

    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.remaining = duration

    def enter(self, fighter) -> None:
        fighter.set_attack_phase("ranged_recovery")
        self.remaining = self.duration

    def exit(self, fighter) -> None:
        fighter.set_attack_phase("idle")

    def update(self, fighter, dt: float) -> None:
        fighter.apply_horizontal_input(acceleration=0.18)
        self.remaining -= dt
        if self.remaining <= 0:
            if fighter.on_ground:
                if fighter.has_horizontal_input():
                    fighter.state_machine.change_state(fighter.state_factory.run())
                else:
                    fighter.state_machine.change_state(fighter.state_factory.idle())
            else:
                fighter.state_machine.change_state(fighter.state_factory.fall())
