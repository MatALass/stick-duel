# Stick Duel

[![CI](https://github.com/MatALass/stick-duel/actions/workflows/ci.yml/badge.svg)](https://github.com/MatALass/stick-duel/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](#installation)
[![Pygame](https://img.shields.io/badge/pygame-2.6%2B-green.svg)](#installation)
[![Coverage](https://img.shields.io/badge/tested-24%20tests-success.svg)](#testing)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](#license)

Local 1v1 fighting game built with **Python** and **Pygame**, designed as both a **playable prototype** and a **software engineering project** focused on modular architecture, finite state machines, scene orchestration, and testable combat logic.

---

## Why this project stands out

A lot of small Pygame games are playable, but structurally weak: gameplay, rendering, transitions, combat, and UI often end up mixed together in a single loop that becomes hard to test, hard to extend, and hard to maintain.

**Stick Duel** was built to avoid that.

This repository demonstrates:

- a clean **src-layout Python package**
- a **scene-driven game flow**
- **FSM-based fighter behavior**
- separated combat and effects systems
- automated tests for both logic and match flow
- CI-backed quality checks with linting and coverage

The point of the project is not only to show that the game works, but that the codebase is organized to evolve cleanly.

---

## Demo

### Core match flow

1. Open the main menu
2. Review the controls
3. Go to the player setup screen
4. Choose fighters and player names
5. Launch the match
6. Trade melee and projectile attacks
7. Win by exhausting the opponent's stocks
8. Transition to the victory scene

### Screenshots

Replace or extend these with your final visuals and gameplay GIF:

![Menu](assets/screenshots/menu.png)
![Setup](assets/screenshots/setup.png)
![Gameplay](assets/screenshots/game.png)

**Recommended improvement:** add a short gameplay GIF near the top of the README for stronger recruiter impact.

---

## Gameplay features

### Combat
- Local 1v1 combat
- Melee attacks with startup, active, and recovery phases
- Projectile attacks for ranged fighters
- Knockback and hit reactions
- Stock-based win condition
- Pause / resume support during matches

### Game feel
- Hit freeze
- Screen shake
- Impact particles
- Damage feedback
- Respawn feedback

### Match flow
- Menu scene
- Controls scene
- Player setup scene
- Game scene
- Victory scene

---

## Characters

### Swordsman
- stronger melee profile
- higher close-range pressure
- no projectile

### Archer
- lower melee pressure
- ranged projectile option
- better spacing potential

---

## Controls

### Player 1 (AZERTY)
- `Q` / `D` -> Move
- `Z` -> Jump
- `S` -> Fast fall
- `F` -> Melee
- `G` -> Ranged

### Player 2
- `Left` / `Right` -> Move
- `Up` -> Jump
- `Down` -> Fast fall
- `Enter` -> Melee
- `Right Shift` -> Ranged

### In match
- `Esc` -> Pause / resume

---

## Technical highlights

### 1. Scene-driven architecture

The game flow is modeled explicitly through scenes instead of being hidden inside one oversized runtime loop.

Main transitions:
- `menu`
- `controls`
- `setup`
- `game`
- `victory`

This makes navigation logic easier to reason about, easier to test, and easier to extend.

### 2. FSM-based fighters

Fighters are organized around explicit state transitions rather than loose boolean flags.

Examples of runtime states include:
- idle
- run
- jump
- melee startup / active / recovery
- ranged startup / recovery
- hitstun
- dead
- respawn

This gives the combat layer clearer contracts and makes future extensions significantly more maintainable.

### 3. Modular gameplay systems

The repository separates:
- scene management
- fighter entities
- fighter states
- combat logic
- effects and feedback
- UI helpers

That separation reduces coupling and prevents gameplay code from collapsing into a single monolithic file.

### 4. Verifiable quality

This project is not just playable; it is testable.

The repository includes:
- automated tests
- integration-oriented match-flow checks
- Ruff linting
- GitHub Actions CI
- coverage reporting

That matters because gameplay systems are easy to break when iteration accelerates.

---

## Architecture overview

### Runtime flow

```text
Input
  -> Scene update
  -> Fighter input interpretation
  -> State machine transitions
  -> Combat resolution
  -> Effects triggering
  -> Rendering
```

### Main modules

#### `src/stick_duel/core/`
Core orchestration primitives:
- scene abstractions
- scene manager
- timers
- state machine helpers

#### `src/stick_duel/scenes/`
Top-level game flow:
- menu
- controls
- player setup
- game
- victory

#### `src/stick_duel/entities/`
Gameplay entities and runtime data:
- fighters
- physics body
- animation data
- stats
- input representation

#### `src/stick_duel/fighter_states/`
State definitions and behavior transitions for fighters.

#### `src/stick_duel/combat/`
Combat-specific logic:
- attacks
- collision
- damage
- projectile handling

#### `src/stick_duel/effects/`
Feedback systems:
- hit freeze
- screen shake
- impact particles

#### `src/stick_duel/ui/`
UI widgets and HUD rendering helpers.

---

## Project structure

```text
stick-duel/
├── .github/
│   └── workflows/
├── assets/
├── src/
│   └── stick_duel/
│       ├── combat/
│       ├── core/
│       ├── effects/
│       ├── entities/
│       ├── fighter_states/
│       ├── scenes/
│       ├── ui/
│       ├── game.py
│       └── main.py
├── tests/
├── pyproject.toml
├── run_game.py
└── README.md
```

---

## Installation

### Requirements
- Python 3.11+

### Install locally

```bash
pip install -e .[dev]
```

This installs the project in editable mode with development tooling.

---

## Running the game

### Entry script
```bash
python run_game.py
```

### Module entry
```bash
python -m stick_duel.main
```

### Console script
```bash
stick-duel
```

---

## Testing

Run the full test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=stick_duel --cov-report=term-missing
```

Run linting:

```bash
ruff check .
```

---

## Continuous Integration

GitHub Actions runs:
- Ruff linting
- automated tests
- coverage-enabled test execution

This helps catch gameplay regressions and structural issues early.

---

## Release notes

### v1.0.0 — Initial stable release

Includes:
- local 1v1 combat
- melee and ranged attacks
- scene-driven game loop
- FSM-based fighters
- effects and feedback systems
- package-based project structure
- automated test suite
- CI pipeline

---

## Roadmap

### Short term
- add gameplay GIF to README
- strengthen match-level integration coverage
- enrich HUD and visual polish
- remove remaining runtime debug traces

### Mid term
- improve animation polish
- add sound integration
- deepen character differentiation
- refine balancing and combat tuning

### Long term
- AI opponent
- additional arenas
- more advanced combat interactions
- optional tournament / versus extensions

---

## Known limitations

- local multiplayer only
- no AI opponent yet
- limited content scope compared with a full game release
- visuals are functional but not yet production-grade

---

## Portfolio value

This repository is meant to be useful for two audiences:

- someone who wants to try the game
- someone evaluating code quality, modularity, and engineering decisions

It should be read as a **playable fighting game prototype with a deliberately serious codebase**, not as a quick one-file Pygame demo.

---

## License

MIT License.
