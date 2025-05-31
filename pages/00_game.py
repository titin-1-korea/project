import streamlit as st
import math
import random
import time

# 설정
st.set_page_config(layout="wide")
st.title("🏹 슈팅 게임")

ROWS, COLS = 25, 100
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(0, COLS - 1)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(0, ROWS - 1)

# 각도, 파워 슬라이더
angle = st.slider("화살 각도 (도)", 20, 160, 90)
power = st.slider("화살 파워", 10, 100, 50)

# 포물선 경로 계산 함수
def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 20
    vy = math.sin(math.radians(angle_deg)) * power / 20
    x, y = COLS // 2, ROWS - 2
    t = 0
    while True:
        xt = int(x + vx * t)
        yt = int(y - (vy * t - 0.5 * 0.7 * t ** 2))
        if 0 <= xt < COLS and 0 <= yt < ROWS:
            trajectory.append((xt, yt))
            t += 0.2
        else:
            break
    return trajectory

# 그리드 출력 함수
def render_grid(trajectory, show_all=True):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = st.session_state.target_x, st.session_state.target_y
    if 0 <= tx < COLS and 0 <= ty < ROWS:
        grid[ty][tx] = TARGET_ICON
    fx, fy = COLS // 2, ROWS - 2
    if 0 <= fx < COLS and 0 <= fy < ROWS:
        grid[fy][fx] = ARROW_ICON
    if show_all:
        for x, y in trajectory:
            if 0 <= x < COLS and 0 <= y < ROWS:
                grid[y][x] = PATH_ICON
    else:
        if trajectory:
            x, y = trajectory[-1]
            if 0 <= x < COLS and 0 <= y < ROWS:
                grid[y][x] = PATH_ICON
    return "\n".join("".join(row) for row in grid)

# 예상 경로 미리보기
trajectory = calculate_trajectory(angle, power)
st.subheader("🔍 예상 경로")
st.text(render_grid(trajectory))

# 발사 버튼
if st.button("발사"):
    hit = False
    placeholder = st.empty()
    for i in range(len(trajectory)):
        placeholder.text(render_grid(trajectory[:i+1], show_all=False))
        time.sleep(0.1)
    for x, y in trajectory:
        if abs(x - st.session_state.target_x) <= 1 and abs(y - st.session_state.target_y) <= 1:
            hit = True
            break
    if hit:
        st.success("🎯 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(0, COLS - 1)
        st.session_state.target_y = random.randint(0, ROWS - 1)
    else:
        st.warning("❌ 빗나감")

# 점수 출력
st.subheader(f"🌟 현재 점수: {st.session_state.score}")
