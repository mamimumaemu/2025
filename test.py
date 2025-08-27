import streamlit as st

st.set_page_config(page_title="📺💡 미디어 리터러시 & 가짜 광고 퀴즈 💡📺", layout="centered")

st.title("📺💡 미디어 리터러시 & 가짜 광고 퀴즈 💡📺")
st.write("문제를 하나씩 풀고 제출하면 정답/오답과 효과가 즉시 표시됩니다! 😆✨")

# ===============================
# 문제 데이터
# ===============================
questions = [
    {
        "question": "광고를 판단할 때 출처와 의도를 확인해야 하는 이유는?",
        "options": ["A. 유명인이 만들었으므로", "B. 자극적이어서", "C. 정보 신뢰성과 소비자 보호", "D. 재미있어서"],
        "answer": "C. 정보 신뢰성과 소비자 보호",
        "explanation": "출처와 의도를 반드시 확인해야 안전합니다. 🎯"
    },
    {
        "question": "SNS 광고 “1주일 만에 피부 좋아짐”을 접했을 때 올바른 판단은?",
        "options": ["A. 친구 추천", "B. 출처/근거 확인", "C. 문구가 예쁘면 믿음", "D. 댓글 많으면 신뢰"],
        "answer": "B. 출처/근거 확인",
        "explanation": "과학적 근거 없는 과장 광고는 믿지 말아야 합니다. 🧐"
    },
    {
        "question": "다음 광고 중 가짜 광고는?",
        "options": [
            "1. FDA 승인 완료, 연구로 효과 입증",
            "2. 하루 5분 투자하면 10kg 감량",
            "3. 친환경 성분 100%, 피부 테스트 완료",
            "4. 인스타 유명인 추천, 한정 판매"
        ],
        "answer": "2. 하루 5분 투자하면 10kg 감량",
        "explanation": "현실적으로 불가능한 과장 광고입니다. 🦠"
    },
    {
        "question": "광고가 자극적이고 근거가 없다면?",
        "options": ["A. 무조건 믿음", "B. 의심하고 근거 확인", "C. 친구 따라 구매", "D. 댓글 많으니 신뢰"],
        "answer": "B. 의심하고 근거 확인",
        "explanation": "근거 없는 광고는 의심하고 판단해야 안전합니다. ⚠️"
    },
    {
        "question": "광고를 합리적으로 평가하려면?",
        "options": ["A. 문구/디자인만 보고", "B. 출처/근거/타깃 확인", "C. 유명인 추천만 믿음", "D. SNS 공유 수만 보고"],
        "answer": "B. 출처/근거/타깃 확인",
        "explanation": "출처, 근거, 타깃 적합성 확인이 필수입니다. 🎯"
    }
]

# ===============================
# 세션 상태 초기화
# ===============================
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "score" not in st.session_state:
    st.session_state.score = 0

# ===============================
# 현재 문제
# ===============================
current_question = st.session_state.current_question

if current_question < len(questions):
    q = questions[current_question]
    st.header(f"문제 {current_question + 1}️⃣")
    st.write(q["question"])

    selected_option = st.radio("선택하세요:", q["options"], key=f"q{current_question}")

    # 제출 버튼
    if st.button("제출 ✔️", key=f"submit_{current_question}") and not st.session_state.answered:
        st.session_state.answered = True
        if selected_option == q["answer"]:
            st.success("🎉 정답입니다! 🎉")
            st.balloons()
            st.session_state.score += 1
        else:
            st.error("💀 오답입니다! 💀")
        st.info(f"💡 해설: {q['explanation']}")

    # 다음 문제 버튼
    if st.session_state.answered:
        if st.button("다음 문제 ➡️"):
            st.session_state.current_question += 1
            st.session_state.answered = False

else:
    st.success("🎉 모든 문제 완료! 📚✨")
    st.info(f"🎯 총 점수: {st.session_state.score} / {len(questions)}")
    # 모든 문제 맞았을 때 confetti 효과
    if st.session_state.score == len(questions):
        st.balloons()
        st.success("🏆 만점! 최고예요! 🎉")
    elif st.session_state.score >= len(questions)//2:
        st.success("👍 절반 이상 맞췄어요! 잘했어요! 🎉")
    else:
        st.warning("😅 조금 아쉬워요. 다시 도전해보세요!")
