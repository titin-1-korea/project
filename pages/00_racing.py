import streamlit as st

# 초기 세팅
st.title("🏎️ 스트림릿 자동차 레이싱 게임 🏁")

# 자동차 위치를 세션 상태로 저장
if 'car_position' not in st.session_state:
    st.session_state.car_position = 0

# 트랙 길이 설정
track_length = 20

# 버튼으로 자동차 전진
if st.button("🚗 가속!"):
    st.session_state.car_position += 1

# 자동차 위치 출력
track = ["-"] * track_length
if st.session_state.car_position < track_length:
    track[st.session_state.car_position] = "🚗"
else:
    track[-1] = "🏁"
    st.balloons()
    st.write("🎉 도착! 축하합니다! 🎉")

st.text("".join(track))

# 다시 시작 버튼
if st.button("🔄 다시 시작"):
    st.session_state.car_position = 0
    st.experimental_rerun()
