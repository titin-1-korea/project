import streamlit as st
import math
import random
import time

st.title("🎯 슈팅 게임 - 각도 조절, 목표 맞추기!")

# 격자 크기
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

# 포물선 경로 계산
def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 10
    vy = math.sin(math.radians(angle_deg)) * power / 10
    x, y = COLS // 2, ROWS - 1  # 중앙 하단
    t = 0
    while True:
        xt = int(x + vx * t)
        yt = int(y - (vy * t - 0.5 * 0.8 * t ** 2))
        if 0 <= xt < COLS and 0 <= yt < ROWS:
            trajectory.append((xt, yt))
            # 목표 도달 시 trajectory 멈춤
            if (xt, yt) == (st.session_state.target_x, st.session_state.target_y):
                break
            t += 0.1
        else:
            break
    return trajectory

# 격자 출력
def render_grid(trajectory, blink=False):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = st.session_state.target_x, st.session_state.target_y
    sx, sy = COLS // 2, ROWS - 1
    for x, y in trajectory:
        if (x, y) != (tx, ty):
            grid[y][x] = PATH_ICON
