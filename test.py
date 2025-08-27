import streamlit as st

st.set_page_config(page_title="📺💡 미디어 리터러시 & 가짜 광고 퀴즈 💡📺", layout="centered")

st.title("📺💡 미디어 리터러시 & 가짜 광고 퀴즈 💡📺")
st.write("문제를 하나씩 풀고 제출하면 즉시 정답/오답 확인과 이펙트가 나옵니다! 😆✨")
st.write("💡 힌트: 광고의 출처, 근거, 과장 여부를 잘 생각하세요! 💡")

# ===============================
# 문제 데이터
# ===============================
questions = [
    {
        "question": "다음 중 광고를 판단할 때 **출처와 의도를 확인해야 하는 이유**로 가장 적절한 것은?",
        "options": [
            "A. 광고를 만든 사람이 유명인이라서",
            "B. 광고 내용이 자극적일수록 효과가 좋기 때문에",
            "C. 정보의 신뢰성을 판단하고 소비자를 보호하기 위해",
            "D. 광고가 재미있으면 모두 믿을 수 있기 때문에"
        ],
        "answer": "C. 정보의 신뢰성을 판단하고 소비자를 보호하기 위해",
        "explanation": "광고가 아무리 흥미롭거나 자극적이어도, 출처와 의도를 반드시 확인해야 안전합니다. 🎯"
    },
    {
        "question": "SNS에서 본 “○○ 제품이 사용 1주일 만에 피부가 좋아진다”는 광고를 접했을 때, 올바른 판단 방법은?",
        "options": [
            "A. 친구가 좋다고 했으니 무조건 구매한다",
            "B. 출처, 실험 근거, 과학적 증거를 확인한다",
            "C. 광고 문구가 예쁘면 믿는다",
            "D. 댓글이 많으면 모두 믿는다"
        ],
        "answer": "B. 출처, 실험 근거, 과학적 증거를 확인한다",
        "explanation": "과학적 근거 없는 과장 광고를 믿으면 피해 발생 가능. 출처와 근거 확인 필수! 🧐"
    },
    {
        "question": "다음 광고 중 **가짜 광고**를 고르시오.",
        "options": [
            "1. “이 제품은 FDA 승인 완료, 과학적 연구로 효과 입증됨”",
            "2. “하루 5분만 투자하면 누구나 10kg 감량 가능”",
            "3. “친환경 성분 100%, 피부 테스트 완료”",
            "4. “인스타 유명인 추천, 한정 판매”"
        ],
        "answer": "2. “하루 5분만 투자하면 누구나 10kg 감량 가능”",
        "explanation": "현실적으로 불가능한 과장 광고는 가짜일 가능성이 높습니다. 🦠"
    },
    {
        "question": "광고가 지나치게 자극적이고, 실제 근거가 없는 내용을 담고 있다면 이 광고를 어떻게 판단해야 할까요?",
        "options": [
            "A. 무조건 믿는다",
            "B. 광고를 의심하고 근거 확인 후 판단한다",
            "C. 친구가 좋아하니 따라 산다",
            "D. 댓글이 많으니 신뢰한다"
        ],
        "answer": "B. 광고를 의심하고 근거 확인 후 판단한다",
        "explanation": "근거 없는 광고는 의심하고 판단해야 안전합니다. ⚠️"
    },
    {
        "question": "다음 중 광고를 합리적으로 평가하는 방법으로 가장 적절한 것은?",
        "options": [
            "A. 광고 문구와 디자인만 보고 판단한다",
            "B. 출처, 근거, 타깃 적합성을 확인한다",
            "C. 유명인 추천만 믿는다",
            "D. SNS 공유 수만 보고 판단한다"
        ],
        "answer": "B. 출처, 근거, 타깃 적합성을 확인한다",
        "explanation": "광고를 합리적으로 평가하려면 출처, 근거, 타깃 적합성 등을 확인해야 합니다. 🎯"
    }
]

# ===============================
# 문제 선택
# ===============================
current_question = st.session_state.get("current_question", 0)

if current_question < len(questions):
    q = questions[current_question]
    st.header(f"문제 {current_question + 1}️⃣")
    st.write(q["question"])
    selected_option = st.radio("선택하세요:", q["options"], key=f"q{current_question}")

    if st.button("제출 ✔️"):
        if selected_option == q["answer"]:
            st.success("🎉 정답입니다! 축하합니다! 🎉")
            st.balloons()
        else:
            st.error("💀 오답입니다! 바이러스 감지! 💀")
        st.info(f"💡 해설: {q['explanation']}")

        # 다음 문제로 이동
        if "current_question" not in st.session_state:
            st.session_state.current_question = 0
        st.session_state.current_question += 1
        st.experimental_rerun()
else:
    st.success("🎉 모든 문제 완료! 퀴즈를 마쳤습니다! 📚✨")
