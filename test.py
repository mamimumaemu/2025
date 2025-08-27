import streamlit as st
from PIL import Image
import random
import time

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(page_title="📊 광고 효과 분석 시뮬레이터", layout="wide")

st.title("📢 광고 효과 분석 시뮬레이터")
st.markdown("업로드한 광고 이미지를 기반으로 **AI가 예상 타겟, 광고 효과, 감정 반응**을 시뮬레이션합니다 🎯✨")

# -----------------------
# 광고 이미지 업로드
# -----------------------
uploaded_file = st.file_uploader("📥 광고 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 광고", use_column_width=True)

    st.markdown("---")

    # -----------------------
    # AI 분석 시뮬레이션
    # -----------------------
    with st.spinner("🤖 AI가 광고를 분석 중입니다..."):
        time.sleep(2)  # 분석하는 것처럼 보여주기 위한 딜레이

        # 🎯 예상 타겟 (랜덤 시뮬레이션)
        possible_targets = ["10대 청소년", "20대 대학생", "직장인", "주부", "시니어 세대", "해외 소비자"]
        target = random.choice(possible_targets)

        # 📈 광고 효과 예측 (랜덤 수치)
        reach = random.randint(1000, 5000)  # 예상 도달 수
        conversion = random.randint(50, 500)  # 예상 전환 수
        roi = round(random.uniform(1.0, 5.0), 2)  # 투자 대비 효과

        # 😀 감정 반응 분석
        emotions = {
            "긍정": random.randint(60, 95),
            "부정": random.randint(5, 40)
        }

    # -----------------------
    # 결과 출력
    # -----------------------
    st.subheader("🎯 AI 분석 결과")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📌 예상 타겟**")
        st.success(f"이 광고의 주요 타겟은 **{target}** 입니다!")

        st.markdown("**📈 광고 효과 예측**")
        st.write(f"- 예상 도달 수: {reach}명")
        st.write(f"- 예상 전환 수: {conversion}명")
        st.write(f"- ROI (투자 대비 효과): {roi} 배")

    with col2:
        st.markdown("**😀 감정 반응 분석**")
        st.progress(emotions["긍정"])
        st.write(f"긍정 반응: {emotions['긍정']}%")

        st.progress(emotions["부정"])
        st.write(f"부정 반응: {emotions['부정']}%")

    st.markdown("---")
    st.info("⚡ 이 분석은 데모용 시뮬레이션 결과이며 실제 데이터 기반은 아닙니다.")
