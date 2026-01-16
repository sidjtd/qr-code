# ======================
# GUI + QR CONSTRUCTION
# ======================

import tkinter as tk
from PIL import Image, ImageTk

# Import your modules
from render import render
from draw_finder import draw_finder
from draw_finder import draw_timing

# ----------------------
# QR CONFIG
# ----------------------

N = 21                 # Version 1 QR
tile_px = 20

grid = [[0 for _ in range(N)] for _ in range(N)]
reserved = [[False for _ in range(N)] for _ in range(N)]

# ----------------------
# TK WINDOW SETUP
# ----------------------

root = tk.Tk()
root.title("QR Code")
root.lift()
root.attributes("-topmost", True)

# Force Tk to initialize (macOS fix)
root.update_idletasks()

photo = None
label = None

# ----------------------
# RENDER / REFRESH
# ----------------------

def refresh():
    global photo, label
    img = render(grid, tile_px)
    photo = ImageTk.PhotoImage(img, master=root)

    if label is None:
        label = tk.Label(root, image=photo)
        label.pack()
    else:
        label.config(image=photo)

    # REQUIRED: prevent garbage collection
    label.image = photo

# ----------------------
# QR STRUCTURE
# ----------------------

draw_finder(0, 0, reserved, grid)
draw_finder(0, N - 7, reserved, grid)
draw_finder(N - 7, 0, reserved, grid)
draw_timing(reserved, grid)

# ----------------------
# DATA PLACEMENT ORDER
# ----------------------

positions = []

col = N - 1
up = True

while col > 0:
    if col == 6:        # timing column
        col -= 1

    rows = range(N - 1, -1, -1) if up else range(N)
    for r in rows:
        positions.append((r, col))
        positions.append((r, col - 1))

    up = not up
    col -= 2

# ----------------------
# DATA → BITS
# ----------------------

url = "www.x.com"
bits = []

# Mode: BYTE (0100)
bits.extend([0, 1, 0, 0])

# Length (8 bits)
length_bits = format(len(url), "08b")
bits.extend(int(b) for b in length_bits)

# ASCII bytes
for ch in url:
    byte = format(ord(ch), "08b")
    bits.extend(int(b) for b in byte)

print("Total bits:", len(bits))  # should be 84

bit_i = 0
delay_ms = 10

# ----------------------
# ANIMATED FILL
# ----------------------

def step(pos_i=0):
    global bit_i

    while pos_i < len(positions):
        r, c = positions[pos_i]
        if not reserved[r][c]:
            break
        pos_i += 1

    if pos_i >= len(positions):
        return

    r, c = positions[pos_i]

    if bit_i < len(bits):
        grid[r][c] = bits[bit_i]
        bit_i += 1
    else:
        grid[r][c] = 0   # neutral fill

    refresh()
    root.after(delay_ms, lambda: step(pos_i + 1))

# ----------------------
# START
# ----------------------

refresh()
root.after(delay_ms, step)
root.mainloop()
