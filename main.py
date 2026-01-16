#This is all the GUI window + event loop dependencies
import tkinter as tk
from PIL import Image, ImageTk

#Import my modules
from render import render
from draw_finder import draw_finder

#Grid numbers total
N = 21

#Each grid cell drawn as a 20×20 pixel square.
tile_px = 20

grid = [[0 for _ in range(N)] for _ in range(N)]
reserved = [[False for _ in range(N)] for _ in range(N)]

####### Block off space
for r in range(7):
    for c in range(7):
        reserved[r][c] = True
        #grid[r][c] = 1   # draw it black so you SEE it

#Get my window going
root = tk.Tk()
root.title("QR Code")
root.lift()

#Keep window sticking to the top
root.attributes("-topmost", True)

img = render(grid, tile_px)
photo = ImageTk.PhotoImage(img)

label = tk.Label(root)
label.pack()

def refresh():
    img = render(grid, tile_px)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo  # keep reference so it doesn't disappear

refresh()
x_seconds = 0.1
delay_ms = int(x_seconds * 100)

#QR fill order:
positions = []

col = N - 1
up = True

while col > 0:
    if col == 6:  # skip timing column later (QR rule placeholder)
        col -= 1

    rows = range(N - 1, -1, -1) if up else range(N)
    for r in rows:
        positions.append((r, col))
        positions.append((r, col - 1))

    up = not up
    col -= 2

def step(i=0):
    # advance i until we find a non-reserved cell
    while i < len(positions):
        r, c = positions[i]
        if not reserved[r][c]:
            break
        i += 1

    if i >= len(positions):
        return

    r, c = positions[i]
    grid[r][c] = 1
    refresh()
    root.after(delay_ms, lambda: step(i + 1))

draw_finder(0, 0, reserved, grid)           # top-left
draw_finder(0, N - 7, reserved, grid)       # top-right
draw_finder(N - 7, 0, reserved, grid)       # bottom-left

root.after(delay_ms, step)
root.mainloop()