def render_grid_horizontal_wrap(trajectory, highlight_last=False, wrap_width=80):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = st.session_state.target_x, st.session_state.target_y
    if 0 <= tx < COLS and 0 <= ty < ROWS:
        grid[ty][tx] = TARGET_ICON
    sx, sy = COLS // 2, ROWS - 1
    grid[sy][sx] = ARROW_ICON
    if highlight_last and trajectory:
        x, y = trajectory[-1]
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = PATH_ICON
    else:
        for x, y in trajectory:
            if 0 <= x < COLS and 0 <= y < ROWS:
                grid[y][x] = PATH_ICON

    # 행별 문자열 이어붙이기
    lines = ["".join(row) for row in grid]
    full_line = "".join(lines)

    # 일정 너비마다 줄바꿈
    wrapped = "\n".join([full_line[i:i+wrap_width] for i in range(0, len(full_line), wrap_width)])
    return wrapped
