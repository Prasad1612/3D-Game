# 🕹️ 3D Shooting Game - Ursina Engine

A real-time 3D first-person shooter built using the [Ursina Engine](https://www.ursinaengine.org/). Fight off waves of enemies with limited ammo, a radar system, and a reload mechanism. Includes both regular and boss enemies, a scoring system, and a game over screen.

## 📸 Screenshot
*(Add screenshots here if possible)*

---

## 🚀 Features

- 🔫 **Shooting System**: Fire bullets with limited ammo and reload functionality.
- 🎯 **Crosshair & Radar**: Aim accurately and track enemies via mini radar.
- 💥 **Enemies**:
  - Regular enemies with 1 HP and faster speed.
  - Boss enemies with more HP and slower movement.
- 🧠 **AI Movement**: Enemies track and chase the player.
- 🔊 **Sound Effects**: Fire, hit, and reload sounds.
- 🛑 **Game Over Screen**: Restart (`X`) or Quit (`C`) when health drops to 0.

---

## 🎮 Controls

| Key            | Action              |
|----------------|---------------------|
| `Left Mouse`   | Shoot bullet        |
| `Z`            | Reload weapon       |
| `X` (on death) | Restart game        |
| `C` (on death) | Quit game           |
| `W/A/S/D`      | Move player         |
| `Space`        | Jump                |
| `Mouse`        | Look around         |

---

## 🛠️ Requirements

- Python 3.7+
- Ursina Engine

Install dependencies via pip:

```bash
pip install ursina
