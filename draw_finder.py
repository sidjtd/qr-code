def draw_finder(top, left, reserved, grid):
    # reserve 7x7 area
    for r in range(top, top + 7):
        for c in range(left, left + 7):
            reserved[r][c] = True
            grid[r][c] = 1  # outer 7x7 black

    # inner 5x5 white
    for r in range(top + 1, top + 6):
        for c in range(left + 1, left + 6):
            grid[r][c] = 0

    # inner 3x3 black
    for r in range(top + 2, top + 5):
        for c in range(left + 2, left + 5):
            grid[r][c] = 1
