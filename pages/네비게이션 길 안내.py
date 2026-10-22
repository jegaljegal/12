import streamlit as st

st.set_page_config(
    page_title="학교 지도 및 길 안내", page_icon="🗺️", layout="wide"
)
st.title("🗺️ 네비게이션 길 안내")

ROOM_INFO = {
    "제1과학실": {
        "building": "본관 3층",
        "time": "1분 30초",
        "guide": [
            "본관 중앙 계단으로 3층 이동",
            "오른쪽 복도로 이동",
            "우측 두 번째 문 입장",
        ],
        "note": "실습 도구 주의",
    },
    "제2과학실": {
        "building": "창의관 3층",
        "time": "2분 30초",
        "guide": [
            "본관 2층 구름다리로 창의관 이동",
            "3층으로 올라감",
            "복도 끝 제2과학실 입장",
        ],
        "note": "실험복 착용 필수",
    },
    "음악실": {
        "building": "예술관 2층",
        "time": "2분 00초",
        "guide": [
            "1층 나와 우측 예술관 건물 이동",
            "계단 이용 2층 올라감",
            "정면 방음문 교실 입장",
        ],
        "note": "실내화 착용",
    },
    "미술실": {
        "building": "예술관 1층",
        "time": "1분 40초",
        "guide": ["본관 1층 후문 지나 예술관 이동", "1층 중앙 통로 우측 진입"],
        "note": "앞치마 준비",
    },
    "컴퓨터실": {
        "building": "창의관 2층",
        "time": "1분 10초",
        "guide": [
            "본관 2층 연결통로로 창의관 진입",
            "2층 201호 입장",
        ],
        "note": "음식물 반입 금지",
    },
    "체육관 (강당)": {
        "building": "체육관 1층",
        "time": "3분 00초",
        "guide": [
            "본관 1층 나와 운동장 건너감",
            "체육관 메인 입구 진입",
        ],
        "note": "체육화 착용",
    },
}

col1, col2 = st.columns(2)
with col1:
    start_point = st.selectbox(
        "🚩 출발지:", ["1반 교실 (본관 2층)", "운동장", "본관 입구"]
    )
with col2:
    dest_point = st.selectbox("🎯 목적지:", list(ROOM_INFO.keys()))

if st.button("🚀 길 안내 시작하기", type="primary"):
    info = ROOM_INFO[dest_point]
    st.success(
        f"🎯 **목적지**: {dest_point} ({info['building']}) | 예상 소요 시간: {info['time']}"
    )
    for idx, step in enumerate(info["guide"], 1):
        st.info(f"Step {idx}. {step}")
    st.warning(f"⚠️ **주의사항**: {info['note']}")
