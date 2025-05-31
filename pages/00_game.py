import streamlit as st
import math
import random

st.set_page_config(layout="wide")
st.title("🏹 슈팅 게임 (개선)")

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(20, 80)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(3, 10)

ROWS, COLS = 25, 100
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"

angle = st.slider("화살 각도 (도)", 20, 160, 90)

def calculate_trajectory(angle_deg, power=50):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 30  # 속도 조정
    vy = math.sin(math.radians(angle_deg)) * power / 30
    x, y = COLS // 2, ROWS - 2  # 출발점 약간 위
    t = 0
    while True:
        xt = int(x + vx * t)
        yt = int(y - (vy * t - 0.5 * 0.7 * t ** 2))  # 중력계수 약간 증가
        if 0 <= xt < COLS and 0 <= yt < ROWS:
            trajectory.append((xt, yt))
            t += 0.2  # 작게 증가하여 촘촘하게
        else:
            break
    return trajectory

def render_grid(trajectory):
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = min(max(st.session_state.target_x, 1), COLS-2), min(max(st.session_state.target_y, 1), ROWS-2)
    grid[ty][tx] = TARGET_ICON
    fx, fy = COLS//2, ROWS-2
    grid[fy][fx] = ARROW_ICON
    for x, y in trajectory:
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = PATH_ICON
    return "\n".join("".join(row) for row in grid)

trajectory = calculate_trajectory(angle)
st.subheader("🔍 경로 및 목표")
st.text(render_grid(trajectory))

if st.button("발사"):
    hit = any(abs(x - st.session_state._
