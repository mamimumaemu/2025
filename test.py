import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📢 광고 효과 분석 시뮬레이터 (체험용)")

# 입력
st.sidebar.header("🎯 캠페인 설정")
budget = st.sidebar.slider("예산 (만원)", 100, 1000, 500)
channel = st.sidebar.selectbox("광고 채널", ["유튜브", "인스타그램", "TV", "옥외광고"])
duration = st.sidebar.slider("기간 (주)", 1, 12, 4)
target_age = st.sidebar.selectbox("타겟 연령대", ["10대", "20대", "30대", "40대 이상"])

# 채널별 가중치 (단순화)
channel_weights = {"유튜브": 1.2, "인스타그램": 1.0, "TV": 0.8, "옥외광고": 0.6}

# 가상의 계산
reach = budget * channel_weights[channel] * np.random.uniform(50, 80)
clicks = reach * np.random.uniform(0.01, 0.05)
conversions = clicks * np.random.uniform(0.05, 0.2)
roi = (conversions * 2000) / (budget * 10000)

# 결과
st.subheader("📊 예상 광고 효과")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Reach", f"{int(reach):,}")
col2.metric("Clicks", f"{int(clicks):,}")
col3.metric("Conversions", f"{int(conversions):,}")
col4.metric("ROI", f"{roi:.2f}")

# 그래프
st.subheader("📈 기간별 성과 시뮬레이션")
weeks = np.arange(1, duration+1)
performance = np.cumsum(np.random.randint(100, 500, size=duration))

fig, ax = plt.subplots()
ax.plot(weeks, performance, marker="o", color="purple")
ax.set_xlabel("주차")
ax.set_ylabel("전환 수")
st.pyplot(fig)

st.success("✨ 캠페인 시뮬레이션 완료! 프레젠테이션에 활용해보세요 😎")

