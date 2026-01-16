def draw_finder(top, left, reserved, grid):
    N = len(grid)

    def set_reserved_white(r, c):
        if 0 <= r < N and 0 <= c < N:
            reserved[r][c] = True
            grid[r][c] = 0

    # --- Separator (white, 1-cell thick, only in-bounds) ---
    # Top and bottom separator rows
    for c in range(left - 1, left + 8):
        set_reserved_white(top - 1, c)
        set_reserved_white(top + 7, c)

    # Left and right separator columns
    for r in range(top - 1, top + 8):
        set_reserved_white(r, left - 1)
        set_reserved_white(r, left + 7)

    # --- Finder pattern 7x7 (reserved) ---
    for r in range(top, top + 7):
        for c in range(left, left + 7):
            reserved[r][c] = True
            grid[r][c] = 1  # outer 7x7 black

    for r in range(top + 1, top + 6):
        for c in range(left + 1, left + 6):
            grid[r][c] = 0  # inner 5x5 white

    for r in range(top + 2, top + 5):
        for c in range(left + 2, left + 5):
            grid[r][c] = 1  # inner 3x3 black

def draw_timing(reserved, grid):
    N = len(grid)

    # row 6 (horizontal timing)
    r = 6
    for c in range(N):
        if not reserved[r][c]:
            reserved[r][c] = True
            grid[r][c] = ((c + 1) % 2)# 0,1,0,1...

    # col 6 (vertical timing)
    c = 6
    for r in range(N):
        if not reserved[r][c]:
            reserved[r][c] = True
            grid[r][c] = ((r + 1) % 2)  # 0,1,0,1...