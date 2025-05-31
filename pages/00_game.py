import streamlit as st
import math
import random
import time

# 화면 설정
st.set_page_config(layout="wide")
st.title("🏹 슈팅 게임 - 각도 조절, 경로, 점수!")

# 격자 크기
ROWS, COLS = 20, 50
TARGET_ICON = "🎯"
ARROW_ICON = "🡆"
PATH_ICON = "*"
EMPTY_ICON = "."

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_x' not in st.session_state:
    st.session_state.target_x = random.randint(5, COLS - 5)
if 'target_y' not in st.session_state:
    st.session_state.target_y = random.randint(2, ROWS // 2)

# 각도와 파워 조절
angle = st.slider("화살 각도 (도)", 20, 160, 90)
power = st.slider("화살 파워", 10, 100, 50)

# 포물선 경로 계산
def calculate_trajectory(angle_deg, power):
    trajectory = []
    vx = math.cos(math.radians(angle_deg)) * power / 15
    vy = math.sin(math.radians(angle_deg)) * power / 15
    x, y = COLS // 2, ROWS - 1
    t = 0
    while True:
        xt = int(x + vx * t)
        yt = int(y - (vy * t - 0.5 * 0.7 * t ** 2))
        if 0 <= xt < COLS and 0 <= yt < ROWS:
            trajectory.append((xt, yt))
