import tkinter as tk
import math

class Moon:
    def __init__(self, canvas, x, y, r, sun, mirror_canvas=None):
        self.canvas = canvas
        self.r = r
        self.sun = sun
        self.mirror_canvas = mirror_canvas  # <- Store mirror canvas
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, 
                                         fill="#7F7F7F", 
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

        # Update background and moon color based on proximity to Sun
        self.update_background()

        # for distance calculation
        self.calculate_distance_to_sun()

    def calculate_distance_to_sun(self):
        coords = self.canvas.coords(self.circle)
        mx = (coords[0] + coords[2]) / 2
        my = (coords[1] + coords[3]) / 2

        sx, sy = self.sun.center()

        #calculating distance from the sun to the moon

        distance = (((( mx - sx ) ** 2) + (( my - sy ) ** 2)) ** 0.5)

        if distance > 300 :
            distance = 300 #for percentile purposes, if its above 300 it sets the distance to 300
        
        #the percentile of the eclipse itself (rounded down for easier read)

        eclipsep = math.floor((300 - distance) / 300 * 100)

        print(eclipsep) #for testing purposes, delete on use!!!!!!!!!!
        return distance, (mx, my)
        
    def update_background(self):
        coords = self.canvas.coords(self.circle)
        mx = (coords[0] + coords[2]) / 2
        my = (coords[1] + coords[3]) / 2

        sx, sy = self.sun.center()

        dist = math.sqrt((mx - sx)**2 + (my - sy)**2)

        max_dist = 400

        bg_brightness = max(0, min(255, int((dist / max_dist) * 255)))
        sky_color = int(bg_brightness * 1.3)
        sky_color = max(0, min(255, sky_color))  # clamp to 0-255

        bg_color = f'#{bg_brightness:02x}{bg_brightness:02x}{sky_color:02x}'

        moon_brightness = max(0, min(255, int((dist / max_dist) * 230)))
        moon_color = f'#{moon_brightness:02x}{moon_brightness:02x}{moon_brightness:02x}'
        
        self.canvas.configure(bg=bg_color)
        self.canvas.itemconfig(self.circle, fill=moon_color)
        
        # Update mirror canvas if provided
        if self.mirror_canvas:
            self.mirror_canvas.configure(bg=bg_color)

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
                   bg="#8787af")
canvas.pack()

#brightness test window (to be deleted on use)
testwindow = tk.Tk()
testwindow.title("brightness test")
canvas2 = tk.Canvas(testwindow, width = W, height = H,
                    bg="#8787af")
canvas2.pack()

# Create Sun in center
sun = Sun(canvas, W/2, H/2, 100)

# Create Moon
moon = Moon(canvas, 150, 150, 99, sun, mirror_canvas=canvas2) #delete the mirror_canvas later on use

root.mainloop()
