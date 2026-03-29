# Stick Duel

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A **local 1v1 fighting game** built with Python and Pygame, designed with a strong focus on **clean architecture**, **finite state machines (FSM)**, and **game feel**.

---

## Features

### Gameplay
- 1v1 local multiplayer
- Melee combat (startup / active / recovery)
- Ranged combat (Archer)
- Knockback & hit detection

### Game Feel (AAA-inspired)
- Hit freeze
- Screen shake
- Impact particles

### Architecture
- Finite State Machine (FSM)
- Modular scene system
- Scalable fighter system

---

## Project Structure

```
stick_duel/
├── core/
├── entities/
├── fighter_states/
├── combat/
├── scenes/
├── ui/
├── effects/
└── assets/
```

---

## Installation

```bash
pip install pygame
```

---

## Run

```bash
python run_game.py
```

---

## Controls

### Player 1 (AZERTY)
- Q / D → Move
- Z → Jump
- S → Fast fall
- F → Melee
- G → Ranged

### Player 2
- ← / → → Move
- ↑ → Jump
- ↓ → Fast fall
- Enter → Melee
- Right Shift → Ranged

---

## Characters

### Swordsman
- High melee damage
- Strong knockback
- No ranged attack

### Archer
- Lower melee damage
- Projectile attacks
- Better spacing gameplay

---

## Technical Highlights

- FSM-based character logic
- Decoupled architecture
- Combat system with attack phases
- Game feel system (effects module)

---

## Screenshots

![Menu](assets/screenshots/menu.png)
![Setup](assets/screenshots/setup.png)
![Game](assets/screenshots/game.png)

---

## Roadmap

- [ ] Advanced animations
- [ ] Sound effects
- [ ] AI opponent
- [ ] Combat depth (combos, cancels)
- [ ] UI polish

---

## License

MIT
