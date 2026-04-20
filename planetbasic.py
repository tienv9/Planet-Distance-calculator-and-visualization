import tkinter as tk
import math

# Orbit radius (scaled for display) + real distance from Sun (million km)
# static info - should replace with real time data
# a - semi-major axis (horizontal radius of ellipse)
# b - semi minor axis (vertical radius of ellipse)
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
moon = {
    "Luna": {"orbit": 20, "angle": 60, "speed": 1, "color": "white"}
}

items = {}
positions = {}
selected = {}
planet_drawings = {}
labels = {}

#setup for window
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
sun = canvas.create_oval(CENTER-15, CENTER-15, CENTER+15, CENTER+15, fill="yellow")
items[sun] = "Sun"
positions["Sun"] = (CENTER, CENTER)


#orbit
for name, data in bodies.items():
    if name == "Sun":
        continue

    a, b = data["a"], data["b"]

    planet = canvas.create_oval(0, 0, 0, 0, fill=data["color"])
    label = canvas.create_text(0, 0, text=name, fill="white", font=("Arial", 8))

    items[planet] = name
    planet_drawings[name] = planet
    labels[name] = label

    canvas.create_oval(
        CENTER-a, CENTER-b,
        CENTER+a, CENTER+b,
        outline="white"
    )


moon_item = canvas.create_oval(0, 0, 0, 0, fill="white")
items[moon_item] = "Luna"


def update_positions():
    for name, data in bodies.items():
        if name == "Sun":
            continue

        angle = math.radians(data["angle"])
        a, b = data["a"], data["b"]

        x = CENTER + a * math.cos(angle)
        y = CENTER + b * math.sin(angle)

        canvas.coords(planet_drawings[name], x-6, y-6, x+6, y+6)
        canvas.coords(labels[name], x, y-10)

        positions[name] = (x, y)

    # Moon relative to Earth
    moon_angle = math.radians(moon["Luna"]["angle"])
    ex, ey = positions["Earth"]

    mx = ex + moon["Luna"]["orbit"] * math.cos(moon_angle)
    my = ey + moon["Luna"]["orbit"] * math.sin(moon_angle)

    canvas.coords(moon_item, mx-3, my-3, mx+3, my+3)
    positions["Luna"] = (mx, my)


def on_click(event):
    item = canvas.find_closest(event.x, event.y)[0]

    if item in items:
        name = items[item]

        if name not in selected:
            selected[name] = True

        info_label.config(text=f"Selected: {', '.join(selected.keys())}")

        if len(selected) == 2:
            calculate_distance()


def calculate_distance():
    names = list(selected.keys())
    p1, p2 = names[0], names[1]

    x1, y1 = positions[p1]
    x2, y2 = positions[p2]

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    result_label.config(
        text=f"Distance: {distance:.2f} units ({p1} <-> {p2})"
    )

    selected.clear()

canvas.bind("<Button-1>", on_click)

# initial render
update_positions()

root.mainloop()