import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# -----------------------------
# 한글 폰트 설정 (운영체제에 맞게)
# -----------------------------
plt.rcParams['font.family'] = 'AppleGothic'  # 맥/리눅스
# plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우

st.set_page_config(page_title="AI 광고 효과 분석 시뮬레이터", page_icon="🤖", layout="wide")
st.title("🤖 AI 광고 효과 분석 시뮬레이터")

# -----------------------------
# 광고 업로드
# -----------------------------
st.sidebar.header("📂 광고 업로드")
ad_text = st.sidebar.text_area("광고 문구 입력", "여기에 광고 문구를 작성하세요 ✍️")
ad_image = st.sidebar.file_uploader("광고 이미지 업로드 (선택)", type=["jpg", "png", "jpeg"])

# -----------------------------
# 관심사 키워드 기반 분석
# -----------------------------
interest_map = {
    "음식": ["제로", "맛", "달콤", "커피", "콜라", "치킨"],
    "게임": ["게임", "레벨", "스킨", "랭크"],
    "뷰티": ["화장품", "뷰티", "스킨케어", "립스틱"],
    "여행": ["여행", "휴가", "바다", "항공"],
    "테크": ["스마트폰", "AI", "로봇", "기술"],
    "운동": ["헬스", "운동", "피트니스", "러닝"]
}

def extract_interests(text):
    detected = []
    for category, keywords in interest_map.items():
        if any(word in text for word in keywords):
            detected.append(category)
    if not detected:
        detected = ["일반"]  # 기본값
    return detected

# -----------------------------
# 광고 효과 분석 (랜덤 시뮬레이션)
# -----------------------------
def analyze_effect():
    reach = random.randint(3000, 10000)
    ctr = round(random.uniform(1.0, 5.0), 2)
    conversion = round(random.uniform(0.5, 3.0), 2)
    roi = round(random.uniform(0.5, 3.0), 2)
    return reach, ctr, conversion, roi

# -----------------------------
# 감정 반응 분석
# -----------------------------
def sentiment_analysis():
    positive = random.randint(50, 90)
    negative = 100 - positive
    return positive, negative

# -----------------------------
# 버튼 클릭 시 실행
# -----------------------------
if st.sidebar.button("🔍 광고 분석 시작"):
    st.subheader("🎯 예상 타겟 분석")
    target_age = random.choice(["10대", "20대", "30대", "40대 이상"])
    target_gender = random.choice(["남성", "여성", "모두"])
    interests = extract_interests(ad_text)

    col1, col2, col3 = st.columns(3)
    col1.metric("연령대", target_age)
    col2.metric("성별", target_gender)
    col3.metric("핵심 관심사", " / ".join(interests))

    st.subheader("📊 광고 효과 분석 (시뮬레이션)")
    reach, ctr, conversion, roi = analyze_effect()
    col4, col5, col6, col7 = st.columns(4)
    col4.metric("도달(Reach)", f"{reach:,}")
    col5.metric("클릭률(CTR)", f"{ctr}%")
    col6.metric("전환율(Conversion)", f"{conversion}%")
    col7.metric("ROI", f"{roi}x")

    st.subheader("😊 감정 반응 (긍정/부정) 시뮬레이션")
    positive, negative = sentiment_analysis()
    fig, ax = plt.subplots()
    ax.pie([positive, negative],
           labels=["긍정", "부정"],
           autopct="%1.1f%%",
           colors=["#0984e3", "#d63031"])
    ax.set_title("광고 감정 반응")
    st.pyplot(fig)

    st.success("✅ 광고 분석 완료!")
