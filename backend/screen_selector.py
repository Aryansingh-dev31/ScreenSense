import tkinter as tk
import pyautogui


def select_area():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.configure(bg="black")

    start_x = start_y = 0
    rectangle = None
    selected = None

    canvas = tk.Canvas(root, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    def start(event):
        nonlocal start_x, start_y
        start_x = event.x
        start_y = event.y

    def drag(event):
        nonlocal rectangle

        if rectangle:
            canvas.delete(rectangle)

        rectangle = canvas.create_rectangle(
            start_x,
            start_y,
            event.x,
            event.y,
            outline="red",
            width=3
        )

    def finish(event):
        nonlocal selected

        x1 = min(start_x, event.x)
        y1 = min(start_y, event.y)
        x2 = max(start_x, event.x)
        y2 = max(start_y, event.y)

        selected = (x1, y1, x2, y2)
        root.destroy()

    canvas.bind("<ButtonPress-1>", start)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind("<ButtonRelease-1>", finish)

    root.mainloop()

    if selected:
        screenshot = pyautogui.screenshot()
        cropped = screenshot.crop(selected)
        cropped.save("screenshots/selected.png")

        return "screenshots/selected.png"

    return None
if __name__ == "__main__":
    print(select_area())