from __future__ import annotations

from dataclasses import dataclass

from stick_duel.fighter_states import (
    DeadState,
    FallState,
    HitstunState,
    IdleState,
    JumpState,
    MeleeActiveState,
    MeleeRecoveryState,
    MeleeStartupState,
    RangedActiveState,
    RangedRecoveryState,
    RangedStartupState,
    RespawnState,
    RunState,
)


@dataclass
class FighterStateFactory:
    fighter: object

    def idle(self) -> IdleState:
        return IdleState()

    def run(self) -> RunState:
        return RunState()

    def jump(self) -> JumpState:
        return JumpState()

    def fall(self) -> FallState:
        return FallState()

    def melee_startup(self) -> MeleeStartupState:
        return MeleeStartupState(self.fighter.melee_attack.startup)

    def melee_active(self) -> MeleeActiveState:
        return MeleeActiveState(self.fighter.melee_attack.active)

    def melee_recovery(self) -> MeleeRecoveryState:
        return MeleeRecoveryState(self.fighter.melee_attack.recovery)

    def ranged_startup(self) -> RangedStartupState:
        return RangedStartupState(self.fighter.ranged_attack.startup)

    def ranged_active(self) -> RangedActiveState:
        return RangedActiveState(self.fighter.ranged_attack.active)

    def ranged_recovery(self) -> RangedRecoveryState:
        return RangedRecoveryState(self.fighter.ranged_attack.recovery)

    def hitstun(self) -> HitstunState:
        return HitstunState(self.fighter.hitstun_duration)

    def dead(self) -> DeadState:
        return DeadState()

    def respawn(self) -> RespawnState:
        return RespawnState(0.5)
