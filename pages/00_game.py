import streamlit as st
import math

# 초기화
st.title("🎯 도트 슈팅 게임 (의미 있는 도트 배치)")
st.write("""
마우스(슬라이더)를 사용해 화살의 방향을 조정하세요.  
발사 버튼을 누르면 화살이 자연스러운 방향으로 날아가 표적을 맞춥니다!  
화면은 도트(10000+)로 구성되며, 각 도트는 캐릭터/목표물/배경에 의미있게 배치됩니다.
""")

ROWS = 50  # 화면 행 수
COLS = 100  # 화면 열 수
TOTAL_DOTS = ROWS * COLS

# 목표물 (타겟)
TARGET_PATTERN = [
    "  ###  ",
    " ##### ",
    "#######",
    " ##### ",
    "  ###  ",
]

TARGET_X = 80
TARGET_Y = 10

# 캐릭터 (화살)
ARROW_PATTERN = [
    "  ^  ",
    " /|\\ ",
    "  |  ",
    " / \\ ",
]

# 발사체 경로: 선형으로 '-'로 표현, 화살 끝은 '^'

# 슬라이더로 각도 제어
angle_deg = st.slider("화살 방향(도)", 0, 360, 90)
angle_rad = math.radians(angle_deg)

# 발사 상태 관리
if 'shot' not in st.session_state:
    st.session_state.shot = False
if st.button("발사!"):
    st.session_state.shot = True

# 화면 출력 문자열 생성
grid = ""
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        # 타겟 패턴 그리기
        target_drawn = False
        for dy, pattern_row in enumerate(TARGET_PATTERN):
            for dx, ch in enumerate(pattern_row):
                tx = TARGET_X + dx - len(pattern_row)//2
                ty = TARGET_Y + dy - len(TARGET_PATTERN)//2
                if x == tx and y == ty and ch == '#':
                    row += "#"
                    target_drawn = True
        if target_drawn:
            continue

        # 화살 그리기 (발사 전)
        if not st.session_state.shot:
            arrow_drawn = False
            start_x = COLS // 2
            start_y = ROWS - 5
            for dy, pattern_row in enumerate(ARROW_PATTERN):
                for dx, ch in enumerate(pattern_row):
                    ax = start_x + dx - len(pattern_row)//2
                    ay = start_y + dy
                    if x == ax and y == ay and ch != ' ':
                        row += ch
                        arrow_drawn = True
            if arrow_drawn:
                continue

        # 화살 경로 그리기 (발사 후)
        if st.session_state.shot:
            start_x = COLS // 2
            start_y = ROWS - 1
            dx_rel = x - start_x
            dy_rel = start_y - y
            distance = math.hypot(dx_rel, dy_rel)
            if distance < 50:
                angle_to_point = math.degrees(math.atan2(dy_rel, dx_rel))
                if abs(angle_to_point - angle_deg) < 2:
                    if int(distance) == int(50) - 1:
                        row += "^"  # 화살 끝
                    else:
                        row += "-"  # 화살 경로
                    continue

        # 배경
        row += "."
    grid += row + "\n"

# 출력
st.text(grid)

# 명중 판정
if st.session_state.shot:
    hit = False
    arrow_end_x = int(COLS//2 + math.cos(angle_rad)*50)
    arrow_end_y = int(ROWS-1 - math.sin(angle_rad)*50)
    if TARGET_X - 3 <= arrow_end_x <= TARGET_X + 3 and \
       TARGET_Y - 2 <= arrow_end_y <= TARGET_Y + 2:
        hit = True
    if hit:
        st.success("🎉 명중했습니다! 도파민 충전 완료! 🎉")
    else:
        st.warning("😢 빗나갔습니다. 다시 시도하세요.")

# 리셋 버튼
if st.button("다시하기"):
    st.session_state.shot = False
    st.experimental_rerun()
