import streamlit as st
import random

st.set_page_config(page_title="📺💡미디어 리터러시 퀴즈💡📺", layout="centered")

st.title("📺💡미디어 리터러시 & 가짜 광고 퀴즈💡📺")
st.write("문제를 신중히 읽고 제출하세요!😎✨")
st.write("💡 힌트: 광고의 출처, 근거, 과장 여부를 논리적으로 판단하세요!💡")

# ===============================
# 문제 데이터 (난이도 살짝 높임)
# ===============================
questions = [
    {
        "question": "SNS 광고: “이 제품은 과학적 연구로 100% 효과가 입증되었습니다.”\n광고에 연구 링크와 출처가 제공되지 않은 경우, 가장 합리적인 판단은 무엇인가?",
        "options": [
            "A. ‘과학적 연구’라고 언급했으므로 구매 가능성을 고려한다",
            "B. 친구와 SNS 후기에서 긍정적인 평가가 많으므로 신뢰한다",
            "C. 광고 디자인과 전문성 있는 문구 때문에 신뢰할 수 있다",
            "D. 출처와 근거가 없으므로 다른 자료를 확인하고 비교 후 판단한다"
        ],
        "answer": "D. 출처와 근거가 없으므로 다른 자료를 확인하고 비교 후 판단한다",
        "explanation": "단순 문구나 외형만으로 판단하면 오류 가능성이 크며, 출처와 근거를 반드시 확인하고 추가 정보와 비교해야 합리적임."
    },
    {
        "question": "다이어트 제품 광고: “하루 5분 투자로 누구나 한 달에 10kg 감량 가능합니다.”\n광고 사진이 전문적이고 유명인이 추천했지만, 과학적 근거는 없는 경우, 가장 합리적인 판단은?",
        "options": [
            "A. 현실적으로 가능성이 낮으므로 근거와 추가 자료를 검토 후 판단한다",
            "B. 유명인이 추천했으므로 제품 효과가 입증되었다고 볼 수 있다",
            "C. 광고 이미지가 전문적이므로 신뢰 가능하다",
            "D. 광고 문구가 설득력 있으므로 효과를 기대할 수 있다"
        ],
        "answer": "A. 현실적으로 가능성이 낮으므로 근거와 추가 자료를 검토 후 판단한다",
        "explanation": "유명인 추천과 디자인만으로는 과장 가능성을 배제할 수 없으며, 현실적 근거와 추가 자료 확인이 필요함."
    },
    {
        "question": "화장품 광고: “친환경 성분 100%, 모든 피부 테스트 완료”\n광고 제작사와 인증 기관이 명시되지 않은 경우, 합리적 판단은 무엇인가?",
        "options": [
            "A. 문구가 친환경을 강조하므로 구매 가능성을 고려한다",
            "B. 출처와 인증 정보를 확인하고, 필요 시 동일 제품과 비교 후 판단한다",
            "C. SNS 공유 수가 많으므로 신뢰할 수 있다",
            "D. 친구 추천이 있으므로 구매 가능성을 고려한다"
        ],
        "answer": "B. 출처와 인증 정보를 확인하고, 필요 시 동일 제품과 비교 후 판단한다",
        "explanation": "인증 기관과 출처 확인 후 판단하는 것이 합리적이며, 다른 제품과 비교 후 결정하는 것이 안전함."
    },
    {
        "question": "광고 문구: “사용 1주일 만에 효과를 체감할 수 있음”\n테스트 참여자는 5명뿐이고 통계적 검증이 없는 경우, 가장 합리적인 판단은 무엇인가?",
        "options": [
            "A. 소수 사례라도 가능성이 있으므로 구매 가능성을 고려한다",
            "B. 참여자 수가 적어 단정할 수 없으며, 다른 자료와 비교 후 판단한다",
            "C. 광고 이미지가 전문적이므로 신뢰 가능하다",
            "D. 친구의 긍정적 평가가 있으므로 구매 가능성을 고려한다"
        ],
        "answer": "B. 참여자 수가 적어 단정할 수 없으며, 다른 자료와 비교 후 판단한다",
        "explanation": "표본 수가 적고 검증이 없으면 과장 가능성이 있으며, 다른 자료와 비교 후 판단해야 안전함."
    },
    {
        "question": "광고 평가 시 합리적 판단 순서는 무엇인가?",
        "options": [
            "A. 디자인과 문구를 확인한 후 구매 결정",
            "B. 유명인 추천과 댓글 수를 확인한 후 신뢰 판단",
            "C. 출처 확인고 근거 검토한 뒤 타깃 적합성 확인하고 다른 자료와 비교 후 판단",
            "D. SNS 공유 수와 광고 클릭 수를 확인한 후 구매 판단"
        ],
        "answer": "C. 출처 확인고 근거 검토한 뒤 타깃 적합성 확인하고 다른 자료와 비교 후 판단",
        "explanation": "합리적 판단은 출처, 근거, 타깃 확인 후 다른 자료와 비교하여 최종 결정을 내려야 안전함."
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
