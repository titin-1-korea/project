import streamlit as st
import math
import time
import random

# 게임 설정
st.set_page_config(layout="wide")
st.title("🎯 슈팅 게임")

# 초기 상태 설정
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(10, 90)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(10, 40)

# 각도 입력
angle = st.slider("화살 각도 (도)", 0, 180, 90)

# 발사 버튼
if st.button("발사"):
    # 화살 경로 계산
    trajectory = []
    for t in range(1, 51):
        x = int(50 + t * math.cos(math.radians(angle)))
        y = int(45 - t * math.sin(math.radians(angle)))
        if 0 <= x <= 100 and 0 <= y <= 50:
            trajectory.append((x, y))
        else:
            break

    # 경로 표시
    for _ in range(3):
        grid = [["." for _ in range(101)] for _ in range(51)]
        # 목표물 표시
        tx = st.session_state.target_x
        ty = st.session_state.target_y
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= ty + i < 51 and 0 <= tx + j < 101:
                    grid[ty + i][tx + j] = "#"
        # 경로 표시
        for x, y in trajectory:
            if 0 <= y < 51 and 0 <= x < 101:
                grid[y][x] = "*"
        # 화면 출력
        st.text("\n".join("".join(row) for row in grid))
        time.sleep(1)

    # 명중 확인
    hit = any(abs(x - tx) <= 1 and abs(y - ty) <= 1 for x, y in trajectory)
    if hit:
        st.success("🎯 명중!")
        st.session_state.score += 10
        # 목표물 위치 변경
        st.session_state.target_x = random.randint(10, 90)
        st.session_state.target_y = random.randint(10, 40)
    else:
        st.warning("❌ 빗나갔습니다.")

# 점수 표시
st.write(f"현재 점수: {st.session_state.score}")
