import streamlit as st
from openai import OpenAI

# ------------------------------
# 🔑 OpenAI 클라이언트 초기화
# (API 키는 반드시 secrets.toml에 저장!)
# ------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------
# 🎨 Streamlit UI 설정
# ------------------------------
st.set_page_config(page_title="광고 효과 분석 시뮬레이터", page_icon="📊", layout="wide")
st.title("📊 광고 효과 분석 시뮬레이터")
st.write("업로드한 광고 문구/이미지를 기반으로 **예상 타겟, 광고 효과, 감정 반응(긍정/부정)**을 AI가 분석해줍니다 🚀")

# ------------------------------
# 📂 입력: 광고 텍스트
# ------------------------------
ad_text = st.text_area("📝 광고 문구를 입력하세요", placeholder="예: 여름을 시원하게! 1+1 아이스 아메리카노 ☕️")

# ------------------------------
# 🚀 버튼 클릭 시 분석 실행
# ------------------------------
if st.button("분석 시작"):
    if ad_text.strip() == "":
        st.warning("⚠️ 광고 문구를 입력해주세요!")
    else:
        with st.spinner("AI가 광고 효과를 분석 중입니다... ⏳"):

            # OpenAI Chat API 호출
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert advertising analyst AI."},
                    {"role": "user", "content": f"다음 광고 문구를 분석해줘:\n\n{ad_text}\n\n"
                                                f"출력은 반드시 아래 형식으로:\n"
                                                f"1. 🎯 예상 타겟\n"
                                                f"2. 📈 광고 효과\n"
                                                f"3. 😊 감정 반응 (긍정/부정 비율 %로)"}
                ],
                max_tokens=500,
                temperature=0.7
            )

            analysis_text = response.choices[0].message.content

        # 결과 출력
        st.subheader("🔎 분석 결과")
        st.write(analysis_text)

        # 감정 반응 강조 표시
        if "긍정" in analysis_text:
            st.success("😀 긍정 반응 있음!")
        if "부정" in analysis_text:
            st.error("😟 부정 반응 있음!")
