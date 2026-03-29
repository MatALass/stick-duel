from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class HitstunState(FighterState):
    name = "hitstun"
    allows_input = False
    interruptible = False

    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.remaining = duration

    def enter(self, fighter) -> None:
        fighter.set_attack_phase("idle")
        fighter.melee_contact_consumed = True
        self.remaining = self.duration

    def update(self, fighter, dt: float) -> None:
        self.remaining -= dt
        if self.remaining <= 0:
            if fighter.on_ground:
                if fighter.has_horizontal_input():
                    fighter.state_machine.change_state(fighter.state_factory.run())
                else:
                    fighter.state_machine.change_state(fighter.state_factory.idle())
            else:
                fighter.state_machine.change_state(fighter.state_factory.fall())
