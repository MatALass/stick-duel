from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class FallState(FighterState):
    name = "fall"

    def update(self, fighter, dt: float) -> None:
        fighter.apply_horizontal_input(acceleration=0.7)

        if fighter.try_consume_fast_fall_input():
            fighter.fast_fall()

        if fighter.on_ground:
            if fighter.has_horizontal_input():
                fighter.state_machine.change_state(fighter.state_factory.run())
            else:
                fighter.state_machine.change_state(fighter.state_factory.idle())
