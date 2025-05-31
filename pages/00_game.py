import streamlit as st
import random
import math

# 기본 설정
ROWS, COLS = 20, 60
PLAYER_ICON = "🏹"
TARGET_ICON = "🎯"
ARROW_ICON = "➶"

# 초기 상태 세션 관리
if "target_x" not in st.session_state:
    st.session_state.target_x = random.randint(5, COLS - 5)
if "target_y" not in st.session_state:
    st.session_state.target_y = random.randint(3, ROWS - 5)
if "score" not in st.session_state:
    st.session_state.score = 0
if "shots" not in st.session_state:
    st.session_state.shots = 5
if "angle" not in st.session_state:
    st.session_state.angle = 0

st.title("🎯 화살 쏘기 게임")
st.markdown(f"**점수**: {st.session_state.score} | **남은 화살**: {st.session_state.shots}")

# 각도 슬라이더
angle = st.slider("발사 각도 (좌:-90° 우:+90°)", -90, 90, st.session_state.angle)
st.session_state.angle = angle

# 화면 그리기 함수
def draw_screen(arrow_pos=None):
    grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    grid[st.session_state.target_y][st.session_state.target_x] = TARGET_ICON
    grid[ROWS // 2][10] = PLAYER_ICON
    if arrow_pos:
        ax, ay = arrow_pos
        if 0 <= ax < COLS and 0 <= ay < ROWS:
            grid[ay][ax] = ARROW_ICON
    return "\n".join("".join(row) for row in grid)

# 발사 버튼
if st.button("발사!"):
    if st.session_state.shots > 0:
        st.session_state.shots -= 1
        distance = COLS - 10
        rad = math.radians(angle)
        arrow_x = int(distance * math.cos(rad))
        arrow_y = int(distance * math.sin(rad))
        hit_x = 10 + arrow_x
        hit_y = ROWS // 2 - arrow_y

        # 명중 판정
        if abs(hit_x - st.session_state.target_x) <= 1 and abs(hit_y - st.session_state.target_y) <= 1:
            st.success("🎯 명중! 점수 +10")
            st.session_state.score += 10
            st.session_state.target_x = random.randint(5, COLS - 5)
            st.session_state.target_y = random.randint(3, ROWS - 5)
        else:
            st.warning("❌ 빗나감")
        
        st.markdown(f"```\n{draw_screen((hit_x, hit_y))}\n```")
    else:
        st.warning("💥 화살 소진!")
        st.markdown(f"```\n{draw_screen()}\n```")
else:
    # 기본 화면 출력
    st.markdown(f"```\n{draw_screen()}\n```")

# 추가 버튼들
col1, col2 = st.columns(2)
with col1:
    if st.button("다음 목표 생성"):
        st.session_state.target_x = random.randint(5, COLS - 5)
        st.session_state.target_y = random.randint(3, ROWS - 5)
        st.markdown(f"```\n{draw_screen()}\n```")
with col2:
    if st.button("게임 재시작"):
        st.session_state.score = 0
        st.session_state.shots = 5
        st.session_state.target_x = random.randint(5, COLS - 5)
        st.session_state.target_y = random.randint(3, ROWS - 5)
        st.markdown(f"```\n{draw_screen()}\n```")
