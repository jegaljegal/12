import datetime
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리반 네비게이터",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 커스텀 디자인 설정 (카드 스타일 적용)
st.markdown(
    """
    <style>
    .custom-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .notice-card {
        background-color: #fef3c7;
        border-left: 6px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .main-title {
        color: #1e40af;
        font-weight: 800;
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Gemini AI 설정
ai_client = None
try:
    from google import genai

    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get(
        "GEMINI_API_KEY"
    )
    if api_key:
        ai_client = genai.Client(api_key=api_key)
except Exception:
    ai_client = None

# 4. 데이터 저장 공간 (공지사항)
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        {
            "date": "2026-10-21",
            "period": "3교시",
            "subject": "과학",
            "original": "1반 교실",
            "changed": "제2과학실 (창의관 3층)",
            "note": "실험복 착용 필수",
        },
        {
            "date": "2026-10-22",
            "period": "5교시",
            "subject": "체육",
            "original": "운동장",
            "changed": "체육관 (강당)",
            "note": "우천으로 인한 장소 변경",
        },
    ]

# 5. 시간표 및 교실 정보 데이터
TIMETABLE = {
    "월요일": [
        ("1교시", "국어", "1반 교실"),
        ("2교시", "수학", "1반 교실"),
        ("3교시", "과학", "제1과학실 (본관 3층)"),
        ("4교시", "영어", "영어 전용실 (본관 2층)"),
        ("5교시", "사회", "1반 교실"),
        ("6교시", "체육", "운동장"),
        ("7교시", "동아리", "각 동아리실"),
    ],
    "화요일": [
        ("1교시", "수학", "1반 교실"),
        ("2교시", "국어", "1반 교실"),
        ("3교시", "음악", "음악실 (예술관 2층)"),
        ("4교시", "과학", "1반 교실"),
        ("5교시", "영어", "1반 교실"),
        ("6교시", "역사", "1반 교실"),
        ("7교시", "자율", "1반 교실"),
    ],
    "수요일": [
        ("1교시", "미술", "미술실 (예술관 1층)"),
        ("2교시", "미술", "미술실 (예술관 1층)"),
        ("3교시", "국어", "1반 교실"),
        ("4교시", "수학", "1반 교실"),
        ("5교시", "정보", "컴퓨터실 (창의관 2층)"),
        ("6교시", "정보", "컴퓨터실 (창의관 2층)"),
        ("7교시", "학급회의", "1반 교실"),
    ],
    "목요일": [
        ("1교시", "영어", "1반 교실"),
        ("2교시", "사회", "1반 교실"),
        ("3교시", "수학", "1반 교실"),
        ("4교시", "체육", "체육관"),
        ("5교시", "과학", "제2과학실 (창의관 3층)"),
        ("6교시", "국어", "1반 교실"),
        ("7교시", "한문", "1반 교실"),
    ],
    "금요일": [
        ("1교시", "역사", "1반 교실"),
        ("2교시", "영어", "1반 교실"),
        ("3교시", "수학", "1반 교실"),
        ("4교시", "국어", "1반 교실"),
        ("5교시", "기술가정", "가정실습실 (본관 4층)"),
        ("6교시", "기술가정", "가정실습실 (본관 4층)"),
        ("7교시", "진로", "1반 교실"),
    ],
}

ROOM_INFO = {
    "제1과학실": {
        "location": "본관 3층 중앙",
        "guide": "본관 중앙 계단을 이용해 3층으로 올라간 후 오른쪽 두 번째 교실입니다.",
        "note": "실습 도구 주의, 음료 반입 금지",
    },
    "제2과학실": {
        "location": "창의관 3층",
        "guide": "본관 2층 구름다리로 창의관 이동 후 3층으로 올라가세요.",
        "note": "실험복 착용 필수",
    },
    "음악실": {
        "location": "예술관 2층",
        "guide": "예술관 1층 입구 우측 계단을 이용해 2층으로 올라오세요.",
        "note": "실내화 착용, 악기 조심히 다루기",
    },
    "미술실": {
        "location": "예술관 1층",
        "guide": "예술관 1층 중앙 통로 우측입니다.",
        "note": "앞치마 지참",
    },
    "컴퓨터실": {
        "location": "창의관 2층",
        "guide": "창의관 엘리베이터 옆 201호입니다.",
