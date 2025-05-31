import streamlit as st

# 화면 크기 설정 (도트 해상도)
ROWS = 20
COLS = 40

# 자동차 초기 위치 세션 관리
if 'car_x' not in st.session_state:
    st.session_state.car_x = COLS // 2
if 'car_y' not in st.session_state:
    st.session_state.car_y = ROWS - 2

st.title("🚗 고해상도 도트 자동차 레이싱 (Streamlit) 🚗")

# 방향 선택 (키보드 입력 대신 버튼으로 대체)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        st.session_state.car_x = max(0, st.session_state.car_x - 1)
        st.rerun()
with col2:
    if st.button("⬆️"):
        st.session_state.car_y = max(0, st.session_state.car_y - 1)
        st.rerun()
with col3:
    if st.button("➡️"):
        st.session_state.car_x = min(COLS - 1, st.session_state.car_x + 1)
        st.rerun()

if st.button("⬇️"):
    st.session_state.car_y = min(ROWS - 1, st.session_state.car_y + 1)
    st.rerun()

# 도트 레이싱 트랙 그리기
grid = ""
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        if x == st.session_state.car_x and y == st.session_state.car_y:
            row += "🚗"
        elif y == 0 or y == ROWS - 1 or x == 0 or x == COLS - 1:
            row += "⬛"
        else:
            row += "·"  # 도트
    grid += row + "\n"

# 출력
st.text(grid)

# 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.car_x = COLS // 2
    st.session_state.car_y = ROWS - 2
    st.rerun()
