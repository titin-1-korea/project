import streamlit as st
import random
import math

ROWS, COLS = 20, 60
PLAYER_ICON = "🏹"
TARGET_ICON = "🎯"
ARROW_ICON = "➶"

if "target_x" not in st.session_state:
    st.session_state.target_x = random.randint(5, COLS - 5)
    st.session_state.target_y = random.randint(3, ROWS - 5)
if "score" not in st.session_state:
    st.session_state.score = 0
if "shots" not in st.session_state:
    st.session_state.shots = 5
if "angle" not in st.session_state:
    st.session_state.angle = 0

st.title("🎯 마우스로 각도 조절 슈팅 게임")
st.markdown("**목표물(🎯)을 향해 화살(➶)을 쏘세요!**")
st.text(f"점수: {st.session_state.score} | 남은 화살: {st.session_state.shots}")

angle = st.slider("발사 각도", -90, 90, st.session_state.angle)
st.session_state.angle = angle

if st.button("발사!"):
    if st.session_state.shots > 0:
        st.session_state.shots -= 1
        distance = COLS - 10
        rad = math.radians(angle)
        arrow_x = int(distance * math.cos(rad))
        arrow_y_
