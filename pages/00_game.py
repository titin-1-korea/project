import streamlit as st
import math
import random
import time

# 화면 설정
st.set_page_config(page_title="🎯 슈팅 게임 - 가로 출력", layout="wide")

st.title("🎯 슈팅 게임 - 가로 출력")

# 격자 크기
ROWS, COLS = 20, 100
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
            t += 0.1
        else:
            break
    return trajectory

# 격자 출력
def render_grid(trajectory, highlight_last=False):
    grid = [[EMPTY_ICON for _ in range(COLS)] for _ in range(ROWS)]
    # 타겟
    tx, ty = st.session_state.target_x, st.session_state.target_y
    if 0 <= ty < ROWS and 0 <= tx < COLS:
        grid[ty][tx] = TARGET_ICON
    # 시작 위치
    sx, sy = COLS // 2, ROWS - 1
    grid[sy][sx] = ARROW_ICON
    # 경로
    for x, y in trajectory:
        if 0 <= y < ROWS and 0 <= x < COLS:
            grid[y][x] = PATH_ICON
    # 문자열 생성
    lines = ["".join(row) for row in grid]
    # 가로 출력으로 변경
    grid_text = "\n".join(lines)
    return grid_text

# 경로 계산 및 미리보기
trajectory = calculate_trajectory(angle, power)

# 목표 및 경로 출력 (가로)
st.subheader("🎯 목표물 및 캐릭터 위치 (한 화면 가로 출력)")
st.text_area("한 화면 보기", render_grid([]), height=ROWS * 20)

st.subheader("🔎 경로 미리보기 (한 화면 가로 출력)")
st.text_area("경로", render_grid(trajectory), height=ROWS * 20)

# 발사 버튼
if st.button("발사"):
    hit = False
    placeholder = st.empty()
    for i in range(len(trajectory)):
        placeholder.text(render_grid(trajectory[:i+1]))
        time.sleep(0.05)
    for x, y in trajectory:
        if abs(x - st.session_state.target_x) <= 1 and abs(y - st.session_state.target_y) <= 1:
            hit = True
            break
    if hit:
        st.success("🎯 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(5, COLS - 5)
        st.session_state.target_y = random.randint(3, ROWS - 5)
    else:
        st.warning("❌ 빗나감")

# 점수 표시
st.subheader(f"현재 점수: {st.session_state.score}")
