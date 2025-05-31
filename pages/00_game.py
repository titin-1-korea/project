import streamlit as st
import math

# 게임 초기화
st.title("🎯 도트 슈팅 게임 (Streamlit-only) 🎯")
st.write("""
마우스(슬라이더)를 사용해 화살의 방향을 조정하세요.  
발사 버튼을 누르면 화살이 날아가고 목표물을 맞출 수 있습니다!  
도트 해상도는 10,000개 이상으로 높은 퀄리티를 자랑합니다.  
""")

# 화면 해상도 설정
ROWS = 100
COLS = 100
DOTS_PER_ROW = COLS
TOTAL_DOTS = ROWS * COLS

# 목표물 위치
TARGET_X = 80
TARGET_Y = 20
TARGET_SIZE = 3  # 목표물 크기

# 각도 슬라이더 (0~360도)
angle_deg = st.slider("화살 방향 (도)", min_value=0, max_value=360, value=90, step=1)
angle_rad = math.radians(angle_deg)

# 발사 버튼
if 'shot' not in st.session_state:
    st.session_state.shot = False
if st.button("발사!"):
    st.session_state.shot = True

# 도트화면 그리기
grid = ""
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        # 목표물 그리기 (O)
        if TARGET_X - TARGET_SIZE <= x <= TARGET_X + TARGET_SIZE and TARGET_Y - TARGET_SIZE <= y <= TARGET_Y + TARGET_SIZE:
            row += "O"
        # 화살 경로 그리기 (발사 상태)
        elif st.session_state.shot:
            start_x = COLS // 2
            start_y = ROWS - 1
            dx = x - start_x
            dy = start_y - y
            if dx == 0:
                theta = 90 if dy >= 0 else -90
            else:
                theta = math.degrees(math.atan2(dy, dx))
            distance = math.hypot(dx, dy)
            # 화살 경로 라인
            if abs(theta - angle_deg) < 3 and distance < 50:
                row += "-"
            # 화살 헤드
            elif abs(theta - angle_deg) < 1 and distance < 2:
                row += ">"
            else:
                row += "."
        else:
            row += "."
    grid += row + "\n"

# 출력
st.text(grid)

# 명중 판정
if st.session_state.shot:
    hit = False
    arrow_end_x = int(COLS // 2 + math.cos(angle_rad) * 50)
    arrow_end_y = int(ROWS - 1 - math.sin(angle_rad) * 50)
    if TARGET_X - TARGET_SIZE <= arrow_end_x <= TARGET_X + TARGET_SIZE and \
       TARGET_Y - TARGET_SIZE <= arrow_end_y <= TARGET_Y + TARGET_SIZE:
        hit = True
    if hit:
        st.success("🎉 명중! 도파민 폭발! 🎉")
    else:
        st.warning("😢 빗나갔습니다. 다시 도전!")

# 리셋
if st.button("다시하기"):
    st.session_state.shot = False
    st.experimental_rerun()
