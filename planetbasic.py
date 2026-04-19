import tkinter as tk
import math

# Orbit radius (scaled for display) + real distance from Sun (million km)
# static info - should replace with real time data
# a - semi-major axis (horizontal radius of ellipse)
# b - semi minor axis (vertical radius of ellipse)
planets = { # should be chance to bodies if include the sun
    "Mercury": {"orbit": 40, "distance": 57.9, "color": "gray"},
    "Venus": {"orbit": 70, "distance": 108.2, "color": "orange"},
    "Earth": {"orbit": 100, "distance": 149.6, "color": "blue"},
    "Mars": {"orbit": 140, "distance": 227.9, "color": "red"},
    "Jupiter": {"orbit": 200, "distance": 778.5, "color": "brown"},
    "Saturn": {"orbit": 260, "distance": 1434.0, "color": "gold"},
    "Uranus": {"orbit": 320, "distance": 2871.0, "color": "light blue"},
    "Neptune": {"orbit": 380, "distance": 4495.1, "color": "dark blue"},
}

bodies = {
    "Sol":      {"a": 0,    "b": 0,     "angle": 0,     "speed": 1, "color": "yellow"},
    "Mercury":  {"a": 50,   "b": 45,    "angle": 252.3, "speed": 1, "color": "gray"},
    "Venus":    {"a": 80,   "b": 75,    "angle": 181.2, "speed": 1, "color": "orange"},
    "Earth":    {"a": 120,  "b": 115,   "angle": 100.5, "speed": 1, "color": "blue"},
    "Mars":     {"a": 170,  "b": 160,   "angle": 355.1, "speed": 1, "color": "red"},
    "Ceres":    {"a": 210,  "b": 200,   "angle": 210.7, "speed": 1, "color": "white"},
    "Jupiter":  {"a": 260,  "b": 250,   "angle": 34.8,  "speed": 1, "color": "brown"},
    "Saturn":   {"a": 320,  "b": 310,   "angle": 120.4, "speed": 1, "color": "gold"},
    "Uranus":   {"a": 380,  "b": 370,   "angle": 210.0, "speed": 1, "color": "light blue"},
    "Neptune":  {"a": 440,  "b": 430,   "angle": 300.2, "speed": 1, "color": "dark blue"},
    "Pluto":    {"a": 500,  "b": 460,   "angle": 45.9,  "speed": 1, "color": "light gray"},
    "Eris":     {"a": 560,  "b": 520,   "angle": 130.6, "speed": 1, "color": "pink"},
}

#change to list and add other planet later
moon = {"orbit": 20, "color": "white"}


selected = []
planet_items = {}

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2

root = tk.Tk()
root.title("Interactive Solar System")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

info_label = tk.Label(root, text="Click two planets", font=("Arial", 14))
info_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

# Sun
canvas.create_oval(CENTER-15, CENTER-15, CENTER+15, CENTER+15, fill="yellow")



def on_click(event):
    item = canvas.find_closest(event.x, event.y)[0]

    if item in planet_items:
        planet_name = planet_items[item]

        if planet_name not in selected:
            selected.append(planet_name)

        info_label.config(text=f"Selected: {', '.join(selected)}")

        if len(selected) == 2:
            calculate_distance()

def calculate_distance():
    p1, p2 = selected
    d1 = planets[p1]["distance"]
    d2 = planets[p2]["distance"]

    distance = abs(d1 - d2)

    result_label.config(
        text=f"Distance: {distance:.2f} million km ({p1} ↔ {p2})"
    )

    selected.clear()

angle_offset = 0
for name, data in planets.items():
    orbit = data["orbit"]

    #orbit
    canvas.create_oval(
        CENTER-orbit, CENTER-orbit,
        CENTER+orbit, CENTER+orbit,
        outline="white"
    )

    #planet (fixed angle for now)
    angle = math.radians(angle_offset)
    x = CENTER + orbit * math.cos(angle)
    y = CENTER + orbit * math.sin(angle)

    planet = canvas.create_oval(
        x-6, y-6, x+6, y+6,
        fill=data["color"]
    )

    canvas.create_text(x, y-10, text=name, fill="white", font=("Arial", 8))

    planet_items[planet] = name

    angle_offset += 45

canvas.bind("<Button-1>", on_click)

root.mainloop()