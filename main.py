import streamlit as st

# 🌈 MBTI 데이터 준비
mbti_data = {
    "INTJ": {
        "특징": "🧠 전략적 · 독립적 · 분석적",
        "추천 진로": ["💻 데이터 사이언티스트", "📊 전략 기획자", "🔧 엔지니어"]
    },
    "ENFP": {
        "특징": "🌸 창의적 · 열정적 · 사교적",
        "추천 진로": ["🎨 광고 기획자", "🎥 방송 PD", "📢 마케팅 전문가"]
    },
    "ISTJ": {
        "특징": "📚 체계적 · 책임감 · 현실적",
        "추천 진로": ["💼 회계사", "🏛 공무원", "🔩 엔지니어"]
    },
    "ESFP": {
        "특징": "🎉 활발함 · 즉흥적 · 친근감",
        "추천 진로": ["🎭 배우", "🎊 이벤트 기획자", "👩‍🏫 교사"]
    },
}

# 🎀 앱 타이틀
st.markdown(
    """
    <h1 style="text-align: center; color: #ff69b4;">
    🌟✨ MBTI 기반 진로 추천 웹앱 ✨🌟
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("## 💖 나의 성격을 찾아 ✨ 나의 꿈을 찾자 🌈💼💡")

# 🎨 MBTI 선택 박스
user_mbti = st.selectbox("🔮 당신의 MBTI는 무엇인가요? ✨", list(mbti_data.keys()))

# 📌 선택 결과 표시
if user_mbti:
    st.markdown(f"### 🌟 당신의 MBTI는 **{user_mbti}** ✨")
    st.markdown(f"**💎 특징:** {mbti_data[user_mbti]['특징']}")

    st.markdown("**🌈 어울리는 진로 추천:**")
    for job in mbti_data[user_mbti]["추천 진로"]:
        st.markdown(f"- {job}")

# ⭐ 관심 진로 저장 기능
if "saved_jobs" not in st.session_state:
    st.session_state["saved_jobs"] = []

selected_job = st.selectbox("💡 관심 있는 진로를 골라보세요 🌟", mbti_data[user_mbti]["추천 진로"])

if st.button("💖✨ 관심 진로 저장하기 ✨💖"):
    st.session_state["saved_jobs"].append(selected_job)
    st.success(f"🌸 '{selected_job}' 이(가) 저장되었습니다! 🌈")

# 📂 저장 목록 표시
if st.session_state["saved_jobs"]:
    st.markdown("## 📌 내가 저장한 진로 리스트 💼🌟")
    st.markdown("💖 지금까지 선택한 꿈 목록이에요 ✨✨")
    for s in st.session_state["saved_jobs"]:
        st.markdown(f"👉 {s}")
