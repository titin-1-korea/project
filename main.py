
import streamlit as st

# 제목
st.title("MBTI별 여행지 추천")

# MBTI 선택
mbti = st.selectbox(
    "당신의 MBTI를 선택하세요:",
    ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
     "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
)

# MBTI별 추천 여행지
recommendations = {
    "INTJ": "아이슬란드 - 조용하고 독특한 풍경",
    "INTP": "노르웨이 - 피요르드와 북극의 매력",
    "ENTJ": "뉴욕 - 도시와 도전",
    "ENTP": "도쿄 - 창의적이고 혁신적인 도시",
    "INFJ": "스위스 - 평화로운 자연과 정취",
    "INFP": "뉴질랜드 - 아름다운 대자연",
    "ENFJ": "파리 - 예술과 낭만의 도시",
    "ENFP": "바르셀로나 - 활기찬 문화와 에너지",
    "ISTJ": "독일 - 질서정연한 도시들",
    "ISFJ": "교토 - 전통과 조화",
    "ESTJ": "싱가포르 - 현대적이고 깔끔한 도시",
    "ESFJ": "런던 - 다양한 문화와 즐길 거리",
    "ISTP": "호주 - 모험과 액티비티",
    "ISFP": "발리 - 자연과 휴식",
    "ESTP": "라스베이거스 - 흥미진진한 경험",
    "ESFP": "마이애미 - 파티와 활기찬 분위기"
}

# 추천 결과 출력
if mbti:
    st.subheader(f"{mbti} 유형에게 추천하는 여행지는:")
    st.write(f"🌍 {recommendations[mbti]}")

# 추가 메시지
st.write("다른 MBTI도 선택해보세요!")
