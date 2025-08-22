import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# -----------------------------
# 앱 기본 설정
# -----------------------------
st.set_page_config(page_title="AI 광고 효과 분석 시뮬레이터", page_icon="🤖", layout="wide")
st.title("🤖 AI 광고 효과 분석 시뮬레이터")
st.write("광고를 업로드하면 **예상 타겟, 효과 분석, 감정 반응**을 AI가 시뮬레이션합니다! 🚀")

# -----------------------------
# 광고 업로드
# -----------------------------
st.sidebar.header("📂 광고 업로드")
ad_text = st.sidebar.text_area("광고 문구 입력", "여기에 광고 문구를 작성하세요 ✍️")
ad_image = st.sidebar.file_uploader("광고 이미지 업로드 (선택)", type=["jpg", "png", "jpeg"])

# -----------------------------
# AI 타겟 예측 (간단 시뮬레이션)
# -----------------------------
def predict_target(text):
    ages = ["10대", "20대", "30대", "40대 이상"]
    genders = ["남성", "여성", "모두"]
    interests = ["패션", "게임", "뷰티", "여행", "테크", "음식"]

    return {
        "연령대": random.choice(ages),
        "성별": random.choice(genders),
        "관심사": random.sample(interests, 2)
    }

# -----------------------------
# 광고 효과 분석 (랜덤 기반)
# -----------------------------
def analyze_effect():
    reach = random.randint(1000, 10000)
    ctr = round(random.uniform(0.5, 5.0), 2)  # 클릭률 %
    conversion = round(random.uniform(0.5, 3.0), 2)  # 전환율 %
    roi = round(random.uniform(0.5, 3.0), 2)  # ROI 배율
    return reach, ctr, conversion, roi

# -----------------------------
# 감정 반응 분석 (긍/부정 비율)
# -----------------------------
def sentiment_analysis():
    positive = random.randint(50, 90)
    negative = 100 - positive
    return positive, negative

# -----------------------------
# 버튼 클릭 시 분석 실행
# -----------------------------
if st.sidebar.button("🔍 광고 분석 시작"):
    st.subheader("🎯 예상 타겟 분석")
    target = predict_target(ad_text)
    st.write(f"- 연령대: {target['연령대']}")
    st.write(f"- 성별: {target['성별']}")
    st.write(f"- 관심사: {', '.join(target['관심사'])}")

    st.subheader("📊 광고 효과 분석")
    reach, ctr, conversion, roi = analyze_effect()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("도달률 (Reach)", f"{reach:,}")
    col2.metric("클릭률 (CTR)", f"{ctr}%")
    col3.metric("전환율 (Conversion)", f"{conversion}%")
    col4.metric("ROI", f"{roi}x")

    st.subheader("😊 감정 반응 분석")
    positive, negative = sentiment_analysis()
    fig, ax = plt.subplots()
    ax.pie([positive, negative], labels=["긍정 👍", "부정 👎"], autopct="%1.1f%%", colors=["#6c5ce7", "#d63031"])
    ax.set_title("광고 감정 반응")
    st.pyplot(fig)

    st.success("✅ 광고 분석이 완료되었습니다!")
