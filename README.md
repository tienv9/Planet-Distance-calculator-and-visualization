# 🌌 Interactive Solar System Simulator

A Python-based interactive solar system visualization built with Tkinter.  
This project simulates planetary motion using real orbital periods, allows distance calculations between celestial bodies, and dynamically scales to fit any window size.

This project is inspired by the Artemis II mission and my curiosity about space and our solar system.

---

## ⚠️ Disclaimer

This project uses **static planetary data** and simplified orbital calculations.  
The positions, distances, and motion are **not 100% scientifically accurate**, and the math used is a **surface-level approximation** intended for visualization purposes only.

---

##  Features

-  Realistic orbital motion based on planetary periods  
-  Start / Pause simulation  
-  Adjustable time scale (day, month, year per second)  
-  Click any two bodies to calculate distance  
-  Distance output in:
  - Kilometers
  - Miles
  - Light travel time  
-  Includes Earth's moon (Luna)  
-  Fully responsive UI (auto-scales with window size)  
-  Clickable planets and Sun  

## Quick look
<img width="1817" height="1830" alt="image" src="https://github.com/user-attachments/assets/7ec71578-8f1a-4dee-a2a0-4ad3d78c7606" />


---

## How It Works

- Each planet follows an elliptical orbit defined by:
  - Semi-major axis (`a`)
  - Semi-minor axis (`b`)
- Motion is calculated using:
  - angle += (360 / orbital_period) * delta_time
- Positions are scaled dynamically based on window size for consistent visualization.

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/tienv9/Planet-Distance-calculator-and-visualization.git
cd solar-system-simulator
```
### 2. Run the program
```bash
python main.py
```

## Controls
| Action               | Description                     |
| -------------------- | ------------------------------- |
| Click planet         | Select for distance calculation |
| Click second planet  | Show distance                   |
| Start / Pause button | Toggle simulation               |
| Slider               | Adjust simulation speed         |
| Preset buttons       | Quick time scaling              |


## Tech Stack

- Python
- Tkinter
- Math (trigonometry + basic orbital mechanics)
