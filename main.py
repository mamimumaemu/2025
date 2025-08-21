import streamlit as st
import pandas as pd

# MBTI 유형과 진로 추천 데이터
mbti_data = {
    "INTJ": {"특징": "전략적, 독립적, 분석적", "추천 진로": ["데이터 사이언티스트", "전략 기획자", "엔지니어"]},
    "ENFP": {"특징": "창의적, 열정적, 사교적", "추천 진로": ["광고 기획자", "방송 PD", "마케팅 전문가"]},
    "ISTJ": {"특징": "체계적, 책임감, 현실적", "추천 진로": ["회계사", "공무원", "엔지니어"]},
    "ESFP": {"특징": "활발함, 즉흥적, 친근감", "추천 진로": ["배우", "이벤트 기획자", "교사"]},
}

# Streamlit 앱 시작
st.title("🌟 MBTI 기반 진로 추천 웹 앱")
st.write("자신의 MBTI 유형을 선택하고, 어울리는 진로를 확인해보세요!")

# MBTI 선택
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_data.keys()))

if user_mbti:
    st.subheader(f"📌 {user_mbti} 유형")
    st.write("**특징:**", mbti_data[user_mbti]["특징"])
    st.write("**추천 진로:**")
    for job in mbti_data[user_mbti]["추천 진로"]:
        st.markdown(f"- {job}")

# 관심 진로 저장하기
if "saved_jobs" not in st.session_state:
    st.session_state["saved_jobs"] = []

selected_job = st.selectbox("관심 있는 진로를 선택하세요:", mbti_data[user_mbti]["추천 진로"])

if st.button("⭐ 관심 진로 저장"):
    st.session_state["saved_jobs"].append(selected_job)
    st.success(f"{selected_job}이(가) 저장되었습니다!")

# 저장된 진로 목록 표시
if st.session_state["saved_jobs"]:
    st.subheader("내가 저장한 진로 목록")
    st.write(st.session_state["saved_jobs"])

