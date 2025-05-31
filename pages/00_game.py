import streamlit as st
import math
import random
import time

st.title("🎯 슈팅 게임 - 한 화면 가로 출력")

ROWS, COLS = 20, 100  # 가로 길이를 늘렸어요
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(COLS//2, COLS-10)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(3, ROWS - 5)

angle = st.slider("각도(도)", 10, 170, 45)
power = st.slider("파워", 10, 100, 50)

def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 10
    vy = math.sin(math.radians(angle_deg)) * power / 10
    x, y = COLS // 2, ROWS - 1
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

def render_grid(trajectory, show_all=True):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = st.session_state.target_x, st.session_state.target_y
    grid[ty][tx] = TARGET_ICON
    sx, sy = COLS // 2, ROWS - 1
    grid[sy][sx] = ARROW_ICON
    for x, y in trajectory:
        grid[y][x] = PATH_ICON
    # 가로 출력 문자열 생성
    lines = ["".join(row) for row in grid]
    return "\n".join(lines)

trajectory = calculate_trajectory(angle, power)

st.subheader("🎯 목표물 및 경로 (한 화면 가로 출력)")
st.text_area("한 화면 보기", render_grid(trajectory), height=ROWS*20)

if st.button("발사"):
    hit = False
    placeholder = st.empty()
    for i in range(len(trajectory)):
        placeholder.text_area("발사 진행", render_grid(trajectory[:i+1]), height=ROWS*20)
        time.sleep(0.05)
    for x, y in trajectory:
        if abs(x - st.session_state.target_x) <= 1 and abs(y - st.session_state.target_y) <= 1:
            hit = True
            break
    if hit:
        st.success("🎯 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(COLS//2, COLS-10)
        st.session_state.target_y = random.randint(3, ROWS - 5)
    else:
        st.warning("❌ 빗나감")

st.subheader(f"현재 점수: {st.session_state.score}")
