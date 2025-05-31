import streamlit as st
import math

# 게임 초기화
st.title("🎯 도트 슈팅 게임 (기록, 남은 화살, 화살 강화)")
st.write("""
슬라이더로 각도를 조절하고 발사 버튼을 눌러 화살을 쏘세요!  
목표물을 맞추면 점수를 얻고 기록이 갱신됩니다!  
남은 화살 수를 주의하세요!  
""")

ROWS, COLS = 50, 100  # 해상도
TARGET_PATTERN = [
    "  ###  ",
    " ##### ",
    "#######",
    " ##### ",
    "  ###  ",
]
TARGET_X, TARGET_Y = 80, 10
ARROW_PATTERN = [
    "  ^  ",
    " /|\\ ",
    "  |  ",
    " / \\ ",
]

MAX_ARROWS = 5

# 상태 초기화
if 'shot' not in st.session_state:
    st.session_state.shot = False
    st.session_state.angle = 90
    st.session_state.arrows_left = MAX_ARROWS
    st.session_state.scores = []  # 이전 기록
    st.session_state.current_score = 0

# 슬라이더 각도 조정
angle_deg = st.slider("화살 각도(도)", 0, 360, st.session_state.angle)
st.session_state.angle = angle_deg
angle_rad = math.radians(angle_deg)

# 발사 버튼
if st.button("발사!"):
    if st.session_state.arrows_left > 0:
        st.session_state.shot = True
        st.session_state.arrows_left -= 1
    else:
        st.warning("💡 화살이 모두 소진되었습니다! '다시하기'를 누르세요.")

# 도트 화면 생성
grid = ""
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        # 목표물
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

        # 화살(발사 전)
        if not st.session_state.shot:
            arrow_drawn = False
            start_x, start_y = COLS//2, ROWS-5
            for dy, pattern_row in enumerate(ARROW_PATTERN):
                for dx, ch in enumerate(pattern_row):
                    ax, ay = start_x + dx - len(pattern_row)//2, start_y + dy
                    if x == ax and y == ay and ch != ' ':
                        row += ch
                        arrow_drawn = True
            if arrow_drawn:
                continue

        # 발사체 경로(발사 후, 강조)
        if st.session_state.shot:
            start_x, start_y = COLS//2, ROWS-1
            dx_rel, dy_rel = x - start_x, start_y - y
            dist = math.hypot(dx_rel, dy_rel)
            if dist < 50:
                angle_to = math.degrees(math.atan2(dy_rel, dx_rel))
                if abs(angle_to - angle_deg) < 1.5:
                    if int(dist) == int(50) - 1:
                        row += "🔺"  # 화살 끝 (강조)
                    else:
                        row += "="  # 경로 강조
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
    if TARGET_X-3 <= arrow_end_x <= TARGET_X+3 and TARGET_Y-2 <= arrow_end_y <= TARGET_Y+2:
        hit = True
    if hit:
        st.success("🎉 명중! 점수 +10점!")
        st.session_state.current_score += 10
    else:
        st.warning("😢 빗나갔습니다.")

# 현재 상태
st.write(f"🎯 남은 화살: {st.session_state.arrows_left}")
st.write(f"🌟 현재 점수: {st.session_state.current_score}")

# 이전 기록
if st.session_state.scores:
    st.write("📜 이전 기록:")
    for i, score in enumerate(st.session_state.scores, 1):
        st.write(f" {i}. {score}점")

# 리셋
if st.button("다시하기"):
    if st.session_state.current_score > 0:
        st.session_state.scores.insert(0, st.session_state.current_score)
    st.session_state.current_score = 0
    st.session_state.arrows_left = MAX_ARROWS
    st.session_state.shot = False
    st.experimental_rerun()

