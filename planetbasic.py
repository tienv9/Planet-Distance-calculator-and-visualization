import tkinter as tk
import math

# Orbit radius (scaled for display) + real distance from Sun (million km)
# static info - should replace with real time data
# a - semi-major axis (horizontal radius of ellipse)
# b - semi minor axis (vertical radius of ellipse)
bodies = {
    "Sol":      {"a": 0,    "b": 0,     "angle": 0,     "speed": 1,      "color": "yellow"},
    "Mercury":  {"a": 50,   "b": 45,    "angle": 252.3, "speed": 88,     "color": "gray"},
    "Venus":    {"a": 80,   "b": 75,    "angle": 181.2, "speed": 225,    "color": "orange"},
    "Earth":    {"a": 120,  "b": 115,   "angle": 100.5, "speed": 365,    "color": "blue"},
    "Mars":     {"a": 170,  "b": 160,   "angle": 355.1, "speed": 687,    "color": "red"},
    "Ceres":    {"a": 210,  "b": 200,   "angle": 210.7, "speed": 1680,   "color": "white"},
    "Jupiter":  {"a": 260,  "b": 250,   "angle": 34.8,  "speed": 4333,   "color": "brown"},
    "Saturn":   {"a": 320,  "b": 310,   "angle": 120.4, "speed": 10759,  "color": "gold"},
    "Uranus":   {"a": 380,  "b": 370,   "angle": 210.0, "speed": 30687,  "color": "light blue"},
    "Neptune":  {"a": 440,  "b": 430,   "angle": 300.2, "speed": 60190,  "color": "dark blue"},
    "Pluto":    {"a": 500,  "b": 460,   "angle": 45.9,  "speed": 90560,  "color": "light gray"},
    "Eris":     {"a": 560,  "b": 520,   "angle": 130.6, "speed": 203600, "color": "pink"},
} #kepler second law make planet move faster need the sun - idea for later

#change to list and add other planet later
moon = {
    "Luna": {"orbit": 20, "angle": 60, "speed": 27.3, "color": "white"}
}

items = {}
positions = {}
selected = {}
planet_drawings = {}
labels = {}
orbit_items = {}

running = False
SIM_SPEED = 10 # default speed of 10 days per seconds
FRAME_TIME = 0.03

AU_TO_KM = 149597870.691 # 1 astronomical unit to km
AU_TO_MILE = 92955807.267433 # 1 astronomical unit to mile
LIGHT_SPEED_KM_S = 299792.458

root = tk.Tk()
root.title("Interactive Solar System")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

info_label = tk.Label(root, text="Click two planets", font=("Arial", 14))
info_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

def get_scale():
    max_a = max(data["a"] for name, data in bodies.items() if name != "Sol")
    size = min(canvas.winfo_width(), canvas.winfo_height())
    return (size * 0.4) / max_a

sun = canvas.create_oval(0, 0, 0, 0, fill="yellow")
items[sun] = "Sol"

def create_orbits_and_planets():
    scale = get_scale()

    for item in orbit_items.values():
        canvas.delete(item)
    orbit_items.clear()

    cx = canvas.winfo_width() // 2
    cy = canvas.winfo_height() // 2

    for name, data in bodies.items():
        if name == "Sol":
            continue

        ap = data["a"] * scale
        bp = data["b"] * scale

        if name not in planet_drawings:
            planet = canvas.create_oval(0, 0, 0, 0, fill=data["color"])
            label = canvas.create_text(0, 0, text=name, fill="white", font=("Arial", 8))

            items[planet] = name
            planet_drawings[name] = planet
            labels[name] = label
            
        orbit = canvas.create_oval(
            cx - ap, cy - bp,
            cx + ap, cy + bp,
            outline="white"
        )
        canvas.tag_lower(orbit)  #push orbit behind everything
        orbit_items[name] = orbit

moon_item = canvas.create_oval(0, 0, 0, 0, fill="white")
items[moon_item] = "Luna"

def update_positions():
    scale = get_scale()
    cx = canvas.winfo_width() // 2
    cy = canvas.winfo_height() // 2

    canvas.coords(sun, cx-12, cy-12, cx+12, cy+12)
    positions["Sol"] = (cx, cy)

    for name, data in bodies.items():
        if name == "Sol":
            continue

        angle = math.radians(data["angle"])

        x = cx + data["a"] * scale * math.cos(angle)
        y = cy + data["b"] * scale * math.sin(angle)

        canvas.coords(planet_drawings[name], x-5, y-5, x+5, y+5)
        canvas.coords(labels[name], x, y-10)

        positions[name] = (x, y)

    ex, ey = positions["Earth"]
    moon_angle = math.radians(moon["Luna"]["angle"])

    mx = ex + moon["Luna"]["orbit"] * scale * math.cos(moon_angle)
    my = ey + moon["Luna"]["orbit"] * scale * math.sin(moon_angle)

    canvas.coords(moon_item, mx-3, my-3, mx+3, my+3)
    positions["Luna"] = (mx, my)

def simulate():
    if not running:
        return

    delta_days = SIM_SPEED * FRAME_TIME

    for name, data in bodies.items():
        if name == "Sol":
            continue

        deg = 360 / data["speed"]
        data["angle"] = (data["angle"] + deg * delta_days) % 360

    moon_deg = 360 / moon["Luna"]["speed"]
    moon["Luna"]["angle"] = (moon["Luna"]["angle"] + moon_deg * delta_days) % 360

    update_positions()
    root.after(int(FRAME_TIME * 1000), simulate)

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
    p1, p2 = list(selected.keys())

    x1, y1 = positions[p1]
    x2, y2 = positions[p2]

    pixel_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

    scale = get_scale()
    distance_au = pixel_distance / (bodies["Earth"]["a"] * scale)

    km = distance_au * AU_TO_KM
    miles = distance_au * AU_TO_MILE

    light_sec = km / LIGHT_SPEED_KM_S
    m = int(light_sec // 60)
    s = int(light_sec % 60)

    result_label.config(
        text=f"{p1} ↔ {p2}\n{km:,.0f} km | {miles:,.0f} mi\nLight: {m}m {s}s"
    )

    selected.clear()

def toggle_simulation():
    global running
    running = not running

    if running:
        simulate()
        btn.config(text="Pause")
    else:
        btn.config(text="Start")

btn = tk.Button(root, text="Start", command=toggle_simulation)
btn.pack()

def update_speed(val):
    global SIM_SPEED
    SIM_SPEED = float(val)

speed_slider = tk.Scale(root, from_=1, to=365, orient="horizontal",
                        resolution=1, command=update_speed)
speed_slider.set(10)
speed_slider.pack()

def set_speed(days):
    global SIM_SPEED
    SIM_SPEED = days
    speed_slider.set(days)

preset_frame = tk.Frame(root)
preset_frame.pack()

tk.Button(preset_frame, text="1 Day/s", command=lambda: set_speed(1)).pack(side="left")
tk.Button(preset_frame, text="10 Day/s", command=lambda: set_speed(10)).pack(side="left")
tk.Button(preset_frame, text="1 Month/s", command=lambda: set_speed(30)).pack(side="left")
tk.Button(preset_frame, text="1 Year/s", command=lambda: set_speed(365)).pack(side="left")

def on_resize(event):
    create_orbits_and_planets()
    update_positions()

canvas.bind("<Configure>", on_resize)
canvas.bind("<Button-1>", on_click)

create_orbits_and_planets()
update_positions()

root.mainloop()