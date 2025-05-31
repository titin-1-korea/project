import streamlit as st
import math
import random

# 게임 초기화
st.set_page_config(layout="wide")
st.title("🎯 슈팅 게임")

# 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(10, 90)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(5, 20)

# 각도 슬라이더
angle = st.slider("화살 각도 (도)", 0, 180, 90)

# 도트 해상도
ROWS, COLS = 25, 100
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"

# 경로 계산
def calculate_trajectory(angle_deg):
    trajectory = []
    for t in range(1, 51):
        x = int(COLS//2 + t * math.cos(math.radians(angle_deg)))
        y = int(ROWS - 1 - t * math.sin(math.radians(angle_deg)))
        if 0 <= x < COLS and 0 <= y < ROWS:
            trajectory.append((x, y))
        else:
            break
    return trajectory

# 경로, 목표, 화살 그리드 출력
def render_grid(trajectory):
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    
    # 목표물
    tx, ty = st.session_state.target_x, st.session_state.target_y
    if 0 <= ty < ROWS and 0 <= tx < COLS:
        grid[ty][tx] = TARGET_ICON
    
    # 화살 출발점
    fx, fy = COLS//2, ROWS - 1
    grid[fy][fx] = ARROW_ICON
    
    # 예상 경로
    for x, y in trajectory:
        if 0 <= y < ROWS and 0 <= x < COLS:
            grid[y][x] = PATH_ICON
    
    # 출력
    return "\n".join("".join(row) for row in grid)

# 예상 경로 계산 및 출력
trajectory = calculate_trajectory(angle)
st.subheader("🔍 예상 경로 및 목표")
st.text(render_grid(trajectory))

# 발사 버튼
if st.button("🎯 화살 발사"):
    hit = any(abs(x - st.session_state.target_x) <= 1 and abs(y - st.session_state.target_y) <= 1 for x, y in trajectory)
    if hit:
        st.success("🎉 명중! 점수 +10")
        st.session_state.score += 10
        st.session_state.target_x = random.randint(10, 90)
        st.session_state.target_y = random.randint(5, 20)
    else:
        st.warning("❌ 빗나갔습니다.")
    # 발사 후 갱신된 화면 출력
    new_trajectory = calculate_trajectory(angle)
    st.text(render_grid(new_trajectory))

# 점수 표시
st.subheader(f"🌟 현재 점수: {st.session_state.score}")

