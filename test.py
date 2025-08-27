import streamlit as st
from PIL import Image
import openai
import io
import matplotlib.pyplot as plt

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(page_title="📊 광고 효과 분석 AI", layout="wide")

st.title("📢 광고 효과 분석 AI")
st.markdown("업로드한 광고 이미지를 기반으로 **실제 AI가 타겟, 광고 효과, 감정 반응**을 분석합니다 🤖✨")

# -----------------------
# OpenAI API 키 입력
# -----------------------
api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")

if api_key:
    openai.api_key = api_key

    # -----------------------
    # 광고 이미지 업로드
    # -----------------------
    uploaded_file = st.file_uploader("📥 광고 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 광고", use_column_width=True)

        st.markdown("---")

        if st.button("🚀 광고 분석 시작하기"):
            with st.spinner("🤖 AI가 광고를 분석 중입니다..."):

                # 이미지를 바이너리로 변환
                img_bytes = io.BytesIO()
                image.save(img_bytes, format="PNG")
                img_bytes = img_bytes.getvalue()

                # -----------------------
                # GPT 모델에 이미지 전달
                # -----------------------
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # 최신 멀티모달 모델
                    messages=[
                        {
                            "role": "system",
                            "content": "너는 전문 광고 기획자이자 소비자 행동 분석가야. 광고 이미지를 분석해서 결과를 제공해."
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "이 광고의 예상 타겟, 광고 효과, 감정 반응을 분석해줘."},
                                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + uploaded_file.getvalue().hex()}}
                            ]
                        }
                    ],
                    max_tokens=500
                )

                result = response["choices"][0]["message"]["content"]

            # -----------------------
            # 결과 출력
            # -----------------------
            st.subheader("🎯 AI 분석 결과")
            st.write(result)

            # 간단 감정 키워드 시각화 (예시: 긍정/부정/흥미)
            emotions = {
                "긍정": result.count("긍정"),
                "부정": result.count("부정"),
                "흥미": result.count("흥미")
            }

            fig, ax = plt.subplots()
            ax.bar(emotions.keys(), emotions.values())
            st.pyplot(fig)
