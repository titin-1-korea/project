import streamlit as st
import math
import random
import time

# 격자 크기 (적당히 한 화면에 보이도록)
ROWS, COLS = 20, 80  
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

# 세션 상태 초기화 및 안전한 좌표 지정
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state or not (0 <= st.session_state.target_x < COLS):
    st.session_state.target_x = random.randint(COLS // 2, COLS - 5)
if 'target_y' not in st.session_state or not (0 <= st.session_state.target_y < ROWS):
    st.session_state.target_y = random.randint(3, ROWS - 5)

# 각도 및 파워 설정
st.title("🎯 슈팅 게임 - 한 화면 가로 출력")
angle = st.slider("각도(도)", 10, 170, 45)
power = st.slider("파워", 10, 100, 50)

# 발사 버튼을 여기로 이동
fire = st.button("발사")

# 포물선 경로 계산
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

# 격자 출력 함수 (좌표 안전하게 처리)
def render_grid(trajectory):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    tx, ty = st.session_state.target_x, st.session_state.target_y
    if 0 <= tx < COLS and 0 <= ty < ROWS:
        grid[ty][tx] = TARGET_ICON
    sx, sy = COLS // 2, ROWS - 1
    if 0 <= sx < COLS and 0 <= sy < ROWS:
        grid[sy][sx] = ARROW_ICON
    for x, y in trajectory:
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = PATH_ICON
    return "\n".join("".join(row) for row in grid)

# 미리보기
trajectory = calculate_trajectory(angle, power)
st.text("🎯 목표물 및 캐릭터 위치 (한 화면 가로 출력)")
st.text_area("한 화면 보기", render_grid([]), height=ROWS*15)
st.text("🔎 경로 미리보기 (한 화면 가로 출력)")
st.text_area("한 화면 보기", render_grid(trajectory), height=ROWS*15)

# 발사 동작
if fire:
    hit = False
    placeholder = st.empty()
    for i in range(len(trajectory)):
        placeholder.text_area("한 화면 보기", render_grid(trajectory[:i+1]), height=ROWS*15)
        time.sleep(0.05)
    for x, y in trajectory:
        if abs(x - st.session_state.target_x) <= 1 and abs(y - st.session_state.target_y) <= 1:
            hit = True
            break
    if hit:
        st.success("🎯 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(COLS // 2, COLS - 5)
        st.session_state.target_y = random.randint(3, ROWS - 5)
    else:
        st.warning("❌ 빗나감")

# 점수 표시
st.subheader(f"현재 점수: {st.session_state.score}")
