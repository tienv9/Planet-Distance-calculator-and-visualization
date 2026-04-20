import tkinter as tk
import math

# Orbit radius (scaled for display) + real distance from Sun (million km)
# static info - should replace with real time data
# a - semi-major axis (horizontal radius of ellipse)
# b - semi minor axis (vertical radius of ellipse)

PIXELS_PER_AU = 120

bodies = {
    "Sol":      {"a": 0.0,      "e": 0,     "angle": 0,     "speed": 1, "color": "yellow"},
    "Mercury":  {"a": 0.39,     "e": 0.206,    "angle": 252.3, "speed": 1, "color": "gray"},
    "Venus":    {"a": 0.72,     "e": 0.007,    "angle": 181.2, "speed": 1, "color": "orange"},
    "Earth":    {"a": 1.00,     "e": 0.017,   "angle": 100.5, "speed": 1, "color": "blue"},
    "Mars":     {"a": 1.52,     "e": 0.093,   "angle": 355.1, "speed": 1, "color": "red"},
    "Ceres":    {"a": 2.77,     "e": 0.076,   "angle": 210.7, "speed": 1, "color": "white"},
    "Jupiter":  {"a": 5.20,     "e": 0.049,   "angle": 34.8,  "speed": 1, "color": "brown"},
    "Saturn":   {"a": 9.58,     "e": 0.056,   "angle": 120.4, "speed": 1, "color": "gold"},
    "Uranus":   {"a": 19.2,     "e": 0.047,   "angle": 210.0, "speed": 1, "color": "light blue"},
    "Neptune":  {"a": 30.1,     "e": 0.009,   "angle": 300.2, "speed": 1, "color": "dark blue"},
    "Pluto":    {"a": 39.5,     "e": 0.248,   "angle": 45.9,  "speed": 1, "color": "light gray"},
    "Eris":     {"a": 67.7,     "e": 0.44,   "angle": 130.6, "speed": 1, "color": "pink"},
}

#change to list and add other planet later
moon = {
    "Luna": {"orbit": 0.00257, "angle": 60, "speed": 1, "color": "white"}
}

items = {}
positions = {}
selected = {}
planet_drawings = {}
labels = {}

AU_TO_KM = 149597870.691 # 1 astronomical unit to km
AU_TO_MILE = 92955807.267433 # 1 astronomical unit to mile
LIGHT_SPEED_KM_S = 299792.458 
SCALE_A = bodies["Earth"]["a"]  # treat as 1 AU

#setup for window
WIDTH, HEIGHT = 900, 900
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
sun = canvas.create_oval(CENTER-10, CENTER-10, CENTER+10, CENTER+10, fill="yellow")
items[sun] = "Sun"
positions["Sun"] = (0, 0)


#orbit
for name, data in bodies.items():
    if name == "Sol":
        continue

    a = data["a"]
    e = data["e"]

    b = a * math.sqrt(1 - e**2)

    # convert to pixels
    ap = a * PIXELS_PER_AU
    bp = b * PIXELS_PER_AU

    canvas.create_oval(
        CENTER-ap, CENTER-bp,
        CENTER+ap, CENTER+bp,
        outline="white"
    )

    planet = canvas.create_oval(0, 0, 0, 0, fill=data["color"])
    label = canvas.create_text(0, 0, text=name, fill="white", font=("Arial", 8))

    items[planet] = name
    planet_drawings[name] = planet
    labels[name] = label

moon_item = canvas.create_oval(0, 0, 0, 0, fill="white")
items[moon_item] = "Luna"


def update_positions():
    for name, data in bodies.items():
        if name == "Sol":
            continue

        angle = math.radians(data["angle"])
        a = data["a"]
        e = data["e"]

        b = a * math.sqrt(1 - e**2)

        # TRUE position in AU
        x_au = a * math.cos(angle)
        y_au = b * math.sin(angle)

        positions[name] = (x_au, y_au)

        # convert to pixels
        x = CENTER + x_au * PIXELS_PER_AU
        y = CENTER + y_au * PIXELS_PER_AU

        canvas.coords(planet_drawings[name], x-4, y-4, x+4, y+4)
        canvas.coords(labels[name], x, y-10)

    # Moon relative to Earth
    moon_angle = math.radians(moon["Luna"]["angle"])
    ex, ey = positions["Earth"]

    mx_au = ex + moon["Luna"]["orbit"] * math.cos(moon_angle)
    my_au = ey + moon["Luna"]["orbit"] * math.sin(moon_angle)

    positions["Luna"] = (mx_au, my_au)

    mx = CENTER + mx_au * PIXELS_PER_AU
    my = CENTER + my_au * PIXELS_PER_AU

    canvas.coords(moon_item, mx-2, my-2, mx+2, my+2)


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

    # Pixel distance (visual)
    distance_au = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Convert to km and mile
    distance_km = distance_au * AU_TO_KM
    distance_mile = distance_au * AU_TO_MILE

    # Light travel time
    time_seconds = distance_km / LIGHT_SPEED_KM_S
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)

    # Convert to minutes + seconds
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)

    result_label.config(
        text=(
            f"{p1} ↔ {p2}\n"
            f"Scaled: {distance_au:.3f} AU\n"
            f"Distance: {distance_km:,.0f} km or {distance_mile:,.0f} mile\n"
            f"Light time: {minutes}m {seconds}s"
        )
    )

    selected.clear()

canvas.bind("<Button-1>", on_click)

# initial render
update_positions()

root.mainloop()