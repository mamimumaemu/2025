import streamlit as st
import random

st.set_page_config(page_title="📺💡 미디어 리터러시 퀴즈 💡📺", layout="centered")

st.title("📺💡 미디어 리터러시 & 가짜 광고 퀴즈 💡📺")
st.write("문제를 신중히 읽고 제출하세요! 😎✨")
st.write("💡 힌트: 광고의 출처, 근거, 과장 여부를 논리적으로 판단하세요! 💡")

# ===============================
# 문제 데이터 (난이도 살짝 높임)
# ===============================
questions = [
    {
        "question": "한 SNS 광고에서 '이 제품을 사용하면 누구나 7일 만에 피부가 완벽해집니다'라고 합니다. 올바른 판단 방법은?",
        "options": [
            "A. 광고 문구만 믿고 구매한다",
            "B. 광고 제작자의 신뢰성과 과학적 근거를 확인한다",
            "C. 댓글 수가 많으면 신뢰한다",
            "D. 친구가 좋다고 하면 바로 구매한다"
        ],
        "answer": "B. 광고 제작자의 신뢰성과 과학적 근거를 확인한다",
        "explanation": "과장된 광고는 반드시 출처와 근거 확인이 필요합니다. 🧐"
    },
    {
        "question": "온라인에서 '하루 5분 투자로 누구나 10kg 감량' 광고를 봤습니다. 이 광고를 평가할 때 가장 합리적인 판단은?",
        "options": [
            "A. 현실적으로 불가능하므로 가짜 광고일 가능성이 높다",
            "B. 유명인이 추천했으므로 믿는다",
            "C. 문구가 예쁘면 효과가 있다",
            "D. 댓글이 많으면 효과가 있다"
        ],
        "answer": "A. 현실적으로 불가능하므로 가짜 광고일 가능성이 높다",
        "explanation": "현실적으로 불가능한 과장 광고는 가짜일 가능성이 큽니다. 🦠"
    },
    {
        "question": "한 광고에서 '친환경 성분 100%, 피부 테스트 완료'라고 합니다. 하지만 출처가 명확하지 않습니다. 이 광고에 대한 판단은?",
        "options": [
            "A. 광고 문구만 믿는다",
            "B. 출처 확인 후 신뢰 여부 판단",
            "C. 유명인이 추천했으니 믿는다",
            "D. 댓글이 많으니 신뢰한다"
        ],
        "answer": "B. 출처 확인 후 신뢰 여부 판단",
        "explanation": "출처가 불분명하면 과장 광고일 수 있으므로 신중하게 판단해야 합니다. ⚠️"
    },
    {
        "question": "광고에서 제품의 효과를 과장하며 실제 근거 없이 홍보한다면, 올바른 판단은?",
        "options": [
            "A. 무조건 믿는다",
            "B. 광고를 의심하고 과학적 근거를 확인한다",
            "C. 친구 추천이면 믿는다",
            "D. 댓글이 많으면 신뢰한다"
        ],
        "answer": "B. 광고를 의심하고 과학적 근거를 확인한다",
        "explanation": "근거 없는 광고는 항상 의심하고 판단해야 안전합니다. ⚠️"
    },
    {
        "question": "광고를 합리적으로 평가하려면 무엇을 가장 먼저 확인해야 할까요?",
        "options": [
            "A. 광고 문구와 디자인만 확인",
            "B. 출처, 근거, 타깃 적합성 확인",
            "C. 유명인 추천만 확인",
            "D. SNS 공유 수만 확인"
        ],
        "answer": "B. 출처, 근거, 타깃 적합성 확인",
        "explanation": "합리적 광고 평가는 출처, 근거, 타깃 적합성을 확인하는 것이 핵심입니다. 🎯"
    }
]

# ===============================
# 세션 상태 초기화
# ===============================
if "remaining_questions" not in st.session_state:
    st.session_state.remaining_questions = list(range(len(questions)))  # 남은 문제 인덱스
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "score" not in st.session_state:
    st.session_state.score = 0

# ===============================
# 다음 문제 선택
# ===============================
def next_question():
    if st.session_state.remaining_questions:
        st.session_state.current_question = random.choice(st.session_state.remaining_questions)
        st.session_state.remaining_questions.remove(st.session_state.current_question)
        st.session_state.answered = False
    else:
        st.session_state.current_question = None

if st.session_state.current_question is None:
    next_question()

# ===============================
# 문제 표시
# ===============================
if st.session_state.current_question is not None:
    q = questions[st.session_state.current_question]
    st.header(f"문제 {len(questions) - len(st.session_state.remaining_questions)}️⃣")
    st.write(q["question"])

    selected_option = st.radio("선택하세요:", q["options"], key=f"q{st.session_state.current_question}")

    # 제출 버튼
    if st.button("제출 ✔️") and not st.session_state.answered:
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
            next_question()
else:
    st.success("🎉 모든 문제 완료! 📚✨")
    st.info(f"🎯 총 점수: {st.session_state.score} / {len(questions)}")
    if st.session_state.score == len(questions):
        st.balloons()
        st.success("🏆 만점! 최고예요! 🎉")
    elif st.session_state.score >= len(questions)//2:
        st.success("👍 절반 이상 맞췄어요! 잘했어요! 🎉")
    else:
        st.warning("😅 조금 아쉬워요. 다시 도전해보세요!")
