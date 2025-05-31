import streamlit as st
import math
import random
import time

st.set_page_config(layout="wide")
st.title("🏹 슈팅 게임")

# 게임 상수 설정
ROWS, COLS = 25, 100
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(0, COLS - 1)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(0, ROWS - 1)

# 각도 및 파워 조절 슬라이더
angle = st.slider("화살 각도 (도)", 20, 160, 90)
power = st.slider("화살 파워", 10, 100, 50)

# 포물선 경로 계산 함수
def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 20
    vy = math.sin(math.radians(angle_deg)) * power / 20
    x, y = COLS //
