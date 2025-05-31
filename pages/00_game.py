import streamlit as st
import math
import random
import time

st.title("🎯 슈팅 게임 - 각도 조절, 목표 맞추기!")

# 격자 크기 설정
ROWS, COLS = 20, 40
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(5, COLS - 5)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(3, ROWS - 5)

# 각도, 파워 조절
angle = st.slider("각도(도)", 10, 170, 45)
power = st.slider("파워", 10, 100, 50)

# 포물선 경로 계산 함수
def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 10
    vy = math.sin(math.radians(angle_deg)) * power / 10
    x, y = COLS // 2, ROWS - 1  # 발사 위치 중앙 하단
    t = 0
    while True:
        xt = int(x + vx * t)
        yt = int(y - (vy * t - 0.5 * 0.8 * t ** 2))
        if 0 <= xt < COLS and 0 <= yt < ROWS:
            trajectory.append((xt, yt))
            t += 0.1
        else:
            break
    return trajectory

# 격자 그리드 생성 함수
def render_grid(trajectory, highlight_last=False):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    # 타겟 표시
    tx, ty = st.session_state.target_x, st.session_state.target_y
    grid[ty][tx] = TARGET_ICON
    # 시작 위치 표시
    sx, sy = COLS // 2, ROWS - 1
    grid[sy][sx] = ARROW_ICON
    # 경로 표시
    if highlight_last and trajectory:
        x, y = trajectory[-1]
        grid[y][x] = PATH_ICON
    else:
        for x, y in trajectory:
            grid[y][x] = PATH_ICON
    return "\n".join("".join(row) for
