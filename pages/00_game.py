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
    # 타겟 깜빡임 처리
    if blink:
        grid[ty][tx] = "💥"
    else:
        grid[ty][tx] = TARGET_ICON
    grid[sy][sx] = ARROW_ICON
    return "\n".join("".join(row) for row in grid)

# 경로 계산 및 미리보기
trajectory = calculate_trajectory(angle, power)
st.text("🎯 목표물 및 캐릭터 위치")
st.text(render_grid([]))
st.text("🔎 경로 미리보기")
st.text(render_grid(trajectory))

# 발사 버튼
if st.button("발사"):
    placeholder = st.empty()
    hit = False
    for i in range(len(trajectory)):
        placeholder.text(render_grid(trajectory[:i+1]))
        time.sleep(0.05)
    # 마지막 경로 지점 확인 (목표물 명중 여부)
    if trajectory and trajectory[-1] == (st.session_state.target_x, st.session_state.target_y):
        hit = True
    if hit:
        # 명중 시 타겟 깜빡이기 애니메이션
        for _ in range(3):
            placeholder.text(render_grid(trajectory, blink=True))
            time.sleep(0.2)
            placeholder.text(render_grid(trajectory, blink=False))
            time.sleep(0.2)
        st.success("🎯 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(5, COLS - 5)
        st.session_state.target_y = random.randint(3, ROWS - 5)
    else:
        st.warning("❌ 빗나감")

# 점수 표시
st.subheader(f"현재 점수: {st.session_state.score}")
