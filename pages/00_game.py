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
st.title("🎯 마우스로 각도 조절 슈

         
