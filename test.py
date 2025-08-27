import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import re
import hashlib
from datetime import datetime

# -----------------------------
# 기본 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 광고 효과 분석 시뮬레이터",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# 유틸: 시드 고정(동일 입력 → 동일 결과)
# -----------------------------
def stable_seed_from_inputs(text: str, image_bytes: bytes | None):
    h = hashlib.sha256()
    h.update((text or "").encode("utf-8"))
    if image_bytes:
        h.update(image_bytes)
    # numpy 난수 시드로 사용
    seed = int(h.hexdigest()[:8], 16)
    np.random.seed(seed)

# -----------------------------
# 유틸: 간단 전처리 & 키워드 추출
# -----------------------------
POSITIVE_WORDS = [
    "할인","특가","한정","신상","인기","프리미엄","추천","혜택","무료","증정",
    "행복","편안","깔끔","상쾌","건강","친환경","안전","맛있","트렌디","고급"
]
NEGATIVE_WORDS = [
    "비싸","불편","오류","지연","부담","리스크","약점","부작용","복잡","실망"
]
AGE_HINTS = {
    "10대": ["학교","시험","입시","패션","아이돌","게임","친구","과자","문구"],
    "20대": ["대학생","알바","취업","연애","카페","뷰티","여행","헬스","노트북"],
    "30대": ["직장인","결혼","육아","재테크","보험","차량","가전","쇼핑","집"],
    "40대 이상": ["건강","병원","연금","골프","프리미엄","효도","안정","숙면","차량"]
}
INTEREST_BANK = [
    "패션","뷰티","게임","여행","테크","음식","운동","음악","학습","재테크","자동차","육아"
]

def tokenize_kor(text: str):
    # 간단 토큰화(공백/특수문자 기준)
    toks = re.findall(r"[가-힣A-Za-z0-9]+", text.lower())
    return toks

# -----------------------------
# AI(시뮬레이션) 분석 로직
# -----------------------------
def predict_target(text: str):
    toks = tokenize_kor(text)
    txt = " ".join(toks)

    # 연령대 추정: 힌트 단어 카운트 최대값
    age_scores = {age: 0 for age in AGE_HINTS}
    for age, hints in AGE_HINTS.items():
        for h in hints:
            if h.lower() in txt:
                age_scores[age] += 1
    age_guess = max(age_scores, key=age_scores.get)

    # 성별 추정(텍스트 키워드 기반 가벼운 휴리스틱)
    female_keys = ["립","마스카라","쿠션","원피스","뷰티","스킨케어","에스테틱"]
    male_keys = ["면도","수트","게임기","스니커즈","엔진","골프","시계"]
    female_score = sum(1 for k in female_keys if k in txt)
    male_score = sum(1 for k in male_keys if k in txt)
    if female_score == male_score:
        gender = "모두"
    elif female_score > male_score:
        gender = "여성"
    else:
        gender = "남성"

    # 관심사: 텍스트 출현 + 랜덤 샘플 보완
    interests_hit = [it for it in INTEREST_BANK if it.lower() in txt]
    remain = [it for it in INTEREST_BANK if it not in interests_hit]
    np.random.shuffle(remain)
    interests = (interests_hit + remain[: max(0, 2 - len(interests_hit))])[:2]

    return {
        "연령대": age_guess,
        "성별": gender,
        "관심사": interests,
    }

def analyze_effect(text: str, has_image: bool):
    # 텍스트 길이/키워드/이미지 유무 등으로 간단 가중치
    length_factor = np.clip(len(text) / 80, 0.5, 2.0)
    pos_hits = sum(1 for w in POSITIVE_WORDS if w in text)
    neg_hits = sum(1 for w in NEGATIVE_WORDS if w in text)
    sentiment_factor = np.clip(1 + 0.05 * (pos_hits - neg_hits), 0.7, 1.3)
    image_boost = 1.15 if has_image else 1.0

    base_reach = np.random.randint(3000, 12000)
    reach = int(base_reach * length_factor * sentiment_factor * image_boost)

    ctr = np.clip(np.random.normal(2.2, 0.8), 0.3, 6.5)          # %
    conversion = np.clip(np.random.normal(1.4, 0.6), 0.2, 4.0)   # %
    # ROI: 도달×CTR×CVR을 간단히 수익-비용 비율로 스케일링
    # (정규화 상수는 보기 좋은 범위를 위한 임의 값)
    roi = np.clip((reach * (ctr/100) * (conversion/100)) / 120, 0.3, 6.0)

    return {
        "reach": int(reach),
        "ctr": round(float(ctr), 2),
        "conversion": round(float(conversion), 2),
        "roi": round(float(roi), 2),
    }

def sentiment_analysis(text: str):
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    # 기본치 + 키워드 기반 가중치 + 작은 노이즈
    base_pos = 60
    score = base_pos + (pos * 6) - (neg * 8) + np.random.randint(-5, 6)
    positive = int(np.clip(score, 5, 95))
    negative = 100 - positive
    return positive, negative

# -----------------------------
# 사이드바: 업로드 & 옵션
# -----------------------------
st.sidebar.header("📂 광고 업로드")
ad_text = st.sidebar.text_area("광고 문구 입력", placeholder="예) 신상 스니커즈 한정 특가! 지금 구매 시 무료 배송 🎁")
ad_image = st.sidebar.file_uploader("광고 이미지 업로드 (선택)", type=["jpg", "jpeg", "png"])

st.sidebar.header("⚙️ 분석 설정")
run_once = st.sidebar.checkbox("버튼 누를 때만 분석 실행", value=True)
analyze_btn = st.sidebar.button("🔍 광고 분석 시작")

# -----------------------------
# 본문: 광고 미리보기
# -----------------------------
with st.expander("👀 업로드 미리보기", expanded=True):
    cols = st.columns([2, 1])
    with cols[0]:
        st.markdown("**광고 문구**")
        if ad_text:
            st.write(ad_text)
        else:
            st.info("광고 문구를 입력하면 여기 표시돼요.")
    with cols[1]:
        st.markdown("**광고 이미지**")
        if ad_image is not None:
            st.image(ad_image, caption="업로드된 광고 이미지", use_column_width=True)
        else:
            st.info("이미지를 선택하지 않아도 분석은 가능합니다.")

# -----------------------------
# 입력 검증
# -----------------------------
def inputs_ready():
    return bool(ad_text and ad_text.strip())

if run_once and not analyze_btn:
    st.warning("왼쪽 사이드바에서 **🔍 광고 분석 시작** 버튼을 눌러주세요.")
elif not inputs_ready():
    st.error("광고 문구를 입력해주세요. (이미지는 선택 사항)")
else:
    # 고정 시드 → 동일 입력은 동일 결과
    image_bytes = ad_image.read() if ad_image is not None else None
    stable_seed_from_inputs(ad_text, image_bytes)

    # -----------------------------
    # 분석 실행
    # -----------------------------
    target = predict_target(ad_text)
    effect = analyze_effect(ad_text, ad_image is not None)
    pos, neg = sentiment_analysis(ad_text)

    # -----------------------------
    # 결과: 타겟 분석
    # -----------------------------
    st.subheader("🎯 예상 타겟 분석")
    c1, c2, c3 = st.columns(3)
    c1.metric("연령대", target["연령대"])
    c2.metric("성별", target["성별"])
    c3.metric("핵심 관심사", " / ".join(target["관심사"]))

    # -----------------------------
    # 결과: 광고 효과 지표
    # -----------------------------
    st.subheader("📊 광고 효과 분석(시뮬레이션)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("도달(Reach)", f"{effect['reach']:,}")
    m2.metric("클릭률(CTR)", f"{effect['ctr']}%")
    m3.metric("전환율(Conversion)", f"{effect['conversion']}%")
    m4.metric("ROI", f"{effect['roi']}x")

    # -----------------------------
    # 그래프: 감정 반응 파이차트
    # -----------------------------
    st.subheader("😊 감정 반응(긍정/부정) 시뮬레이션")
    fig1, ax1 = plt.subplots()
    ax1.pie([pos, neg], labels=["긍정", "부정"], autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # -----------------------------
    # 그래프: 기간별 전환(임의 기간 4주)
    # -----------------------------
    st.subheader("📈 기간별 전환 추이(예시 4주)")
    weeks = np.arange(1, 5)
    base_conv = effect["reach"] * (effect["ctr"]/100) * (effect["conversion"]/100)
    noise = np.random.normal(0.9, 0.15, size=4)
    weekly_conversions = np.maximum(1, (base_conv / 4) * noise).astype(int)

    fig2, ax2 = plt.subplots()
    ax2.plot(weeks, weekly_conversions, marker="o")
    ax2.set_xlabel("주차")
    ax2.set_ylabel("전환 수")
    st.pyplot(fig2)

    # -----------------------------
    # 데이터 테이블 & 다운로드
    # -----------------------------
    st.subheader("📥 결과 데이터 다운로드")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame(
        [{
            "분석시각": now,
            "연령대": target["연령대"],
            "성별": target["성별"],
            "관심사": " / ".join(target["관심사"]),
            "Reach": effect["reach"],
            "CTR(%)": effect["ctr"],
            "Conversion(%)": effect["conversion"],
            "ROI(x)": effect["roi"],
            "긍정(%)": pos,
            "부정(%)": neg,
            "주1 전환": int(weekly_conversions[0]),
            "주2 전환": int(weekly_conversions[1]),
            "주3 전환": int(weekly_conversions[2]),
            "주4 전환": int(weekly_conversions[3]),
            "문구(미리보기)": (ad_text[:80] + "…") if len(ad_text) > 80 else ad_text,
            "이미지사용": "Y" if ad_image is not None else "N",
        }]
    )
    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="CSV 다운로드",
        data=csv_bytes,
        file_name="ad_analysis_result.csv",
        mime="text/csv"
    )

    st.success("✅ 광고 분석이 완료되었습니다! (동일 입력은 동일 결과로 재현 가능)")

# 푸터
st.caption("※ 본 앱은 교육·시뮬레이션 목적이며, 실제 매체 성과를 보장하지 않습니다.")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# -----------------------------
# 한글 폰트 설정 (운영체제에 맞게)
# -----------------------------
plt.rcParams['font.family'] = 'AppleGothic'  # 맥/리눅스
# plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우

st.set_page_config(page_title="AI 광고 효과 분석 시뮬레이터", page_icon="🤖", layout="wide")
st.title("🤖 AI 광고 효과 분석 시뮬레이터")

# -----------------------------
# 광고 업로드
# -----------------------------
st.sidebar.header("📂 광고 업로드")
ad_text = st.sidebar.text_area("광고 문구 입력", "여기에 광고 문구를 작성하세요 ✍️")
ad_image = st.sidebar.file_uploader("광고 이미지 업로드 (선택)", type=["jpg", "png", "jpeg"])

# -----------------------------
# 관심사 키워드 기반 분석
# -----------------------------
interest_map = {
    "음식": ["제로", "맛", "달콤", "커피", "콜라", "치킨"],
    "게임": ["게임", "레벨", "스킨", "랭크"],
    "뷰티": ["화장품", "뷰티", "스킨케어", "립스틱"],
    "여행": ["여행", "휴가", "바다", "항공"],
    "테크": ["스마트폰", "AI", "로봇", "기술"],
    "운동": ["헬스", "운동", "피트니스", "러닝"]
}

def extract_interests(text):
    detected = []
    for category, keywords in interest_map.items():
        if any(word in text for word in keywords):
            detected.append(category)
    if not detected:
        detected = ["일반"]  # 기본값
    return detected

# -----------------------------
# 광고 효과 분석 (랜덤 시뮬레이션)
# -----------------------------
def analyze_effect():
    reach = random.randint(3000, 10000)
    ctr = round(random.uniform(1.0, 5.0), 2)
    conversion = round(random.uniform(0.5, 3.0), 2)
    roi = round(random.uniform(0.5, 3.0), 2)
    return reach, ctr, conversion, roi

# -----------------------------
# 감정 반응 분석
# -----------------------------
def sentiment_analysis():
    positive = random.randint(50, 90)
    negative = 100 - positive
    return positive, negative

# -----------------------------
# 버튼 클릭 시 실행
# -----------------------------
if st.sidebar.button("🔍 광고 분석 시작"):
    st.subheader("🎯 예상 타겟 분석")
    target_age = random.choice(["10대", "20대", "30대", "40대 이상"])
    target_gender = random.choice(["남성", "여성", "모두"])
    interests = extract_interests(ad_text)

    col1, col2, col3 = st.columns(3)
    col1.metric("연령대", target_age)
    col2.metric("성별", target_gender)
    col3.metric("핵심 관심사", " / ".join(interests))

    st.subheader("📊 광고 효과 분석 (시뮬레이션)")
    reach, ctr, conversion, roi = analyze_effect()
    col4, col5, col6, col7 = st.columns(4)
    col4.metric("도달(Reach)", f"{reach:,}")
    col5.metric("클릭률(CTR)", f"{ctr}%")
    col6.metric("전환율(Conversion)", f"{conversion}%")
    col7.metric("ROI", f"{roi}x")

    st.subheader("😊 감정 반응 (긍정/부정) 시뮬레이션")
    positive, negative = sentiment_analysis()
    fig, ax = plt.subplots()
    ax.pie([positive, negative],
           labels=["긍정", "부정"],
           autopct="%1.1f%%",
           colors=["#0984e3", "#d63031"])
    ax.set_title("광고 감정 반응")
    st.pyplot(fig)

    st.success("✅ 광고 분석 완료!")
