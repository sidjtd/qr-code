import tkinter as tk
from PIL import Image, ImageTk

tile_px = 200
grid = [[0]]  # 1x1 white tile

def render(grid, tile_px):
    h, w = len(grid), len(grid[0])
    img = Image.new("RGB", (w * tile_px, h * tile_px), "white")
    px = img.load()
    for r in range(h):
        for c in range(w):
            color = (0, 0, 0) if grid[r][c] == 1 else (255, 255, 255)
            x0, y0 = c * tile_px, r * tile_px
            for y in range(y0, y0 + tile_px):
                for x in range(x0, x0 + tile_px):
                    px[x, y] = color
    return img

root = tk.Tk()
root.title("White Tile")

root.lift()
root.attributes("-topmost", True)
#root.after(200, lambda: root.attributes("-topmost", False))

img = render(grid, tile_px)
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
