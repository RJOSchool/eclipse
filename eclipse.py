import tkinter as tk
import math

class Moon:
    def __init__(self, canvas, x, y, r, sun):
        self.canvas = canvas
        self.r = r
        self.sun = sun
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, 
                                         fill="gray", 
                                         outline="")
        self._drag_data = {"x": 0, "y": 0}

        # Bind events
        canvas.tag_bind(self.circle, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(self.circle, "<B1-Motion>", self.on_drag)

    def on_press(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]

        self.canvas.move(self.circle, dx, dy)

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        # Update background based on proximity to Sun
        self.update_background()

    def update_background(self):
        # Get Moon center position
        coords = self.canvas.coords(self.circle)
        mx = (coords[0] + coords[2]) / 2
        my = (coords[1] + coords[3]) / 2

        # Get Sun center position
        sx, sy = self.sun.center()

        # Calculate distance
        dist = math.sqrt((mx - sx)**2 + (my - sy)**2)

        # Map distance to brightness (closer = brighter)
        max_dist = 400
        brightness = max(0, min(255, int((dist / max_dist) * 255)))
        color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'  # grayscale

        self.canvas.configure(bg=color)

class Sun:
    def __init__(self, canvas, x, y, r):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, 
                                         fill="yellow", 
                                         outline="")

    def center(self):
        return self.x, self.y

# Set up the window
root = tk.Tk()
root.title("Sun and Moon Proximity")

W = 600
H = 600
canvas = tk.Canvas(root, width=W, height=H, 
                   bg="white")
canvas.pack()

# Create Sun in center
sun = Sun(canvas, W/2, H/2, 100)

# Create Moon
moon = Moon(canvas, 150, 150, 100, sun)

root.mainloop()
