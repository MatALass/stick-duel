from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class RunState(FighterState):
    name = "run"

    def update(self, fighter, dt: float) -> None:
        fighter.apply_horizontal_input(acceleration=1.1)

        if fighter.try_consume_jump_input():
            fighter.state_machine.change_state(fighter.state_factory.jump())
            return

        if fighter.try_consume_melee_input() and fighter.can_start_melee():
            fighter.start_melee_sequence()
            return

        if fighter.try_consume_ranged_input() and fighter.can_start_ranged():
            fighter.start_ranged_sequence()
            return

        if fighter.try_consume_fast_fall_input():
            fighter.fast_fall()

        if not fighter.on_ground:
            fighter.state_machine.change_state(fighter.state_factory.fall())
            return

        if not fighter.has_horizontal_input():
            fighter.state_machine.change_state(fighter.state_factory.idle())
