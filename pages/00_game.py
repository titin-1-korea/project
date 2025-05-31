import streamlit as st
import random
import math

# 화면 크기 설정
ROWS, COLS = 20, 60

# 캐릭터, 목표물, 발사체 설정
PLAYER_ICON = "🏹"
TARGET_ICON = "🎯"
ARROW_ICON = "➶"

# 초기 상태 설정
if "target_x" not in st.session_state:
    st.session_state.target_x = random.randint(5, COLS - 5)
    st.session_state.target_y = random.randint(3, ROWS - 5)
if "score" not in st.session_state:
    st.session_state.score = 0
if "shots" not in st.session_state:
    st.session_state.shots = 5
if "angle" not in st.session_state:
    st.session_state.angle = 0

# 화면 설명
st.title("🎯 마우스로 각도 조절 슈팅 게임")
st.markdown("**목표물(🎯)을 향해 화살(➶)을 쏘세요! 각도는 마우스로 조절합니다.**")
st.text(f"점수: {st.session_state.score} | 남은 화살: {st.session_state.shots}")

# 각도 입력 슬라이더
angle = st.slider("발사 각도", -90, 90, st.session_state.angle)
st.session_state.angle = angle

# '발사' 버튼
if st.button("발사!"):
    if st.session_state.shots > 0:
        st.session_state.shots -= 1
        # 화살 경로 계산
        distance = COLS - 10  # 화살 최대 거리
        rad = math.radians(angle)
        arrow_x = int(distance * math.cos(rad))
        arrow_y = int(distance * math.sin(rad))
        hit_x = 10 + arrow_x
        hit_y = ROWS // 2 - arrow_y

        # 화면 그리드 생성
        grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        # 목표물 표시
        grid[st.session_state.target_y][st.session_state.target_x] = TARGET_ICON
        # 플레이어 표시
        grid[ROWS // 2][10] = PLAYER_ICON
        # 화살 표시
        if 0 <= hit_x < COLS and 0 <= hit_y < ROWS:
            grid[hit_y][hit_x] = ARROW_ICON

        # 명중 여부
        if abs(hit_x - st.session_state.target_x) <= 1 and abs(hit_y - st.session_state.target_y) <= 1:
            st.success("🎯 명중! 점수 +10")
            st.session_state.score += 10
        else:
            st.warning("❌ 빗나감")

        # 그리드 출력
        st.text("\n".join("".join(row) for row in grid))
    else:
        st.warning("💥 화살이 모두 소진되었습니다!")

# '다음 목표물 생성' 버튼
if st.button("다음 목표물 생성"):
    st.session_state.target_x = random.randint(5, COLS - 5)
    st.session_state.target_y = random.randint(3, ROWS - 5)

# 게임 재시작 버튼
if st.button("게임 재시작"):
    st.session_state.score = 0
    st.session_state.shots = 5
    st.session_state.target_x = random.randint(5, COLS - 5)
    st.session_state.target_y = random.randint(3, ROWS - 5)
