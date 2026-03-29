from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class JumpState(FighterState):
    name = "jump"

    def enter(self, fighter) -> None:
        fighter.perform_jump()

    def update(self, fighter, dt: float) -> None:
        fighter.apply_horizontal_input(acceleration=0.7)

        if fighter.try_consume_fast_fall_input():
            fighter.fast_fall()

        if fighter.body.velocity_y >= 0:
            fighter.state_machine.change_state(fighter.state_factory.fall())
