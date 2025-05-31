import streamlit as st
import random
import time
import math

# 게임 화면 크기
ROWS, COLS = 20, 30

# 이모지
TARGET_ICON = "🎯"
PLAYER_ICON = "🏹"
ARROW_ICON = "➤"

# 초기화
if "target_x" not in st.session_state:
    st.session_state.target_x = random.randint(20, COLS - 3)  # 목표물 위치
if "target_y" not in st.session_state:
    st.session_state.target_y = random.randint(5, ROWS - 5)
if "score" not in st.session_state:
    st.session_state.score = 0
if "shots" not in st.session_state:
    st.session_state.shots = 5

# 각도 슬라이더
angle = st.slider("각도를 조절하세요", -45, 45, 0)

# 발사 버튼
if st.button("발사!") and st.session_state.shots > 0:
    st.session_state.shots -= 1

    # 발사체 경로 계산
    trajectory = []
    x, y = 1, ROWS // 2
    radians = math.radians(angle)
    dx = math.cos(radians)
    dy = -math.sin(radians)
    for step in range(1, COLS):
        x_pos = int(x + dx * step)
        y_pos = int(y + dy * step)
        if 0 <= x_pos < COLS and 0 <= y_pos < ROWS:
            trajectory.append((y_pos, x_pos))
        else:
            break

    # 목표물에 맞았는지 확인
    hit = False
    for ty, tx in trajectory:
        if (tx, ty) == (st.session_state.target_x, st.session_state.target_y):
            hit = True
            break

    if hit:
        st.session_state.score += 1
        st.session_state.target_x = random.randint(15, COLS - 3)
        st.session_state.target_y = random.randint(5, ROWS - 5)
        st.success("🎯 명중!")
    else:
        st.warning("놓쳤어요!")

    # 화면 그리기
    grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    grid[ROWS // 2][1] = PLAYER_ICON
    grid[st.session_state.target_y][st.session_state.target_x] = TARGET_ICON
    for ty, tx in trajectory:
        grid[ty][tx] = ARROW_ICON
    display = "\n".join("".join(row) for row in grid)
    st.text(display)
    time.sleep(3)  # 3초 후 초기화
else:
    # 기본 화면 출력
    grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    grid[ROWS // 2][1] = PLAYER_ICON
    grid[st.session_state.target_y][st.session_state.target_x] = TARGET_ICON
    st.text("\n".join("".join(row) for row in grid))

# 점수 및 남은
