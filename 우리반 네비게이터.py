import datetime
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리반 네비게이터",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 커스텀 CSS 디자인
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .custom-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .custom-card-blue {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 2px solid #93c5fd;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .notice-card {
        background-color: #fffbeb;
        border-left: 6px solid #f59e0b;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .step-box {
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Session State 데이터 관리
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        {
            "id": 1,
            "date": "2026-10-21",
            "period": "3교시",
            "subject": "과학",
            "teacher": "유우석 선생님",
            "original": "12반 교실",
            "changed": "제2과학실 (본관 5층)",
            "note": "실험복 착용 필수 및 보안경 지참",
        },
        {
            "id": 2,
            "date": "2026-10-22",
            "period": "5교시",
            "subject": "체육",
            "teacher": "이학용 선생님",
            "original": "운동장",
            "changed": "체육관 (강당)",
            "note": "우천으로 인한 장소 변경",
        },
    ]

# 4. 학급 및 특별실 데이터
TIMETABLE = {
    "월요일": [
        ("1교시", "국어", "백근영", "12반 교실", "교과서, 공책"),
        ("2교시", "수학", "김지은", "12반 교실", "수학익힘책"),
        ("3교시", "과학", "주민지", "제1과학실 (본관 3층)", "실험관찰"),
        ("4교시", "영어", "이윤재", "영어 전용실 (본관 2층)", "영어 교재"),
        ("5교시", "사회", "김지영", "12반 교실", "사회과 탐구"),
        ("6교시", "체육", "이학용", "운동장", "체육복"),
        ("7교시", "한국사", "최이환", "12반 교실", "역사 프린트물"),
    ],
    "화요일": [
        ("1교시", "수학", "김지은", "12반 교실", "수학익힘책"),
        ("2교시", "국어", "백근영", "12반 교실", "교과서"),
        ("3교시", "음악", "김현희", "음악실 (예술관 2층)", "리코더"),
        ("4교시", "과학", "김종운", "12반 교실", "과학 교과서"),
        ("5교시", "영어", "이윤재", "12반 교실", "영어 단어장"),
        ("6교시", "역사", "최이환", "12반 교실", "역사 노트"),
        ("7교시", "자율", "담임(김민서)", "12반 교실", "활동지"),
    ],
    "수요일": [
        ("1교시", "미술", "유제은", "미술실 (예술관 1층)", "수채화 도구"),
        ("2교시", "미술", "유제은", "미술실 (예술관 1층)", "수채화 도구"),
        ("3교시", "국어", "백근영", "12반 교실", "교과서"),
        ("4교시", "수학", "김지은", "12반 교실", "수학익힘책"),
        ("5교시", "정보", "김미나", "정보실 (본관 5층)", "USB"),
        ("6교시", "정보", "김미나", "정보실 (본관 5층)", "USB"),
        ("7교시", "학급회의", "담임(김민서)", "12반 교실", "안건지"),
    ],
    "목요일": [
        ("1교시", "영어", "이윤재", "12반 교실", "영어 교과서"),
        ("2교시", "사회", "정기운", "12반 교실", "지도책"),
        ("3교시", "수학", "김지은", "12반 교실", "수학익힘책"),
        ("4교시", "체육", "이학용", "체육관", "체육화"),
        ("5교시", "과학", "유우석", "제2과학실 (창의관 3층)", "실험복"),
        ("6교시", "국어", "백근영", "12반 교실", "교과서"),
        ("7교시", "기술가정", "임헌열", "12반 교실", "프린트물"),
    ],
    "금요일": [
        ("1교시", "역사", "최이환", "12반 교실", "역사 교과서"),
        ("2교시", "영어", "이윤재", "12반 교실", "프린트"),
        ("3교시", "수학", "김지은", "12반 교실", "수학익힘책"),
        ("4교시", "국어", "백근영", "12반 교실", "교과서"),
        ("5교시", "동아리", "담당교사", "각 동아리실", "프린트물"),
        ("6교시", "동아리", "담당교사", "각 동아리실", "프린트물"),
    ],
}

ROOM_INFO = {
    "제1과학실": {
        "location": "본관 5층 복도 안쪽",
        "guide": "본관 중앙 계단을 이용해 3층으로 올라간 후 오른쪽 두 번째 교실입니다.",
        "equipment": "현미경, 알코올램프, 실험대, 환기장치",
        "teacher": "주민지 선생님",
        "note": "실습 도구 사용 주의, 음료 및 음식물 반입 금지",
    },
    "제2과학실": {
        "location": "본관 5층 중앙",
        "guide": "본관 5층에서 중앙 복도를 통해 들어가세요.",
        "equipment": "화학 실험대, 안전 시약장, 긴급 세안기",
        "teacher": "유우석 선생님",
        "note": "실험복 착용 필수, 실험 중 자리 이탈 금지",
    },
    "음악실": {
        "location": "본관 5층 정면",
        "guide": "본관 5층 입구 우측에 방음으로 된 문으로 들어가세요.",
        "equipment": "그랜드 피아노, 각종 타악기, 앰프 시스템",
        "teacher": "김현희 선생님",
        "note": "실내화 필수 착용, 악기 무단 조작 금지",
    },
    "미술실": {
        "location": "본관 5층 복도 끝",
        "guide": "본관 5층 중앙 통로 우측입니다.",
        "equipment": "이젤, 물감 세척대, 석고상, 작업대",
        "teacher": "유제은 선생님",
        "note": "앞치마 착용 권장, 물 사용 후 개수대 청소 필수",
    },
    "정보실": {
        "location": "본관 5층 (미술실 옆)",
        "guide": "본관 5층에서 복도 안쪽으로 이동합니다.",
        "equipment": "최신 PC 40대, 빔프로젝터, 프린터",
        "teacher": "김미나 선생님",
        "note": "음식물 반입 금지, 착석 후 PC 점검 필수",
    },
    "체육관 (강당)": {
        "location": "체육관 2층",
        "guide": "12반 교실에서 나와 복도 따라 직진하세요.",
        "equipment": "농구대, 배드민턴 네트, 매트, 방송실",
        "teacher": "이학용 선생님",
        "note": "체육화(깨끗한 운동화) 필수 착용",
    },
}

# 5. 사이드바 메뉴
st.sidebar.image(
    "https://img.icons8.com/color/96/school.png", use_container_width=False
)
st.sidebar.title("📌 네비게이션")

menu = st.sidebar.radio(
    "원하는 페이지를 선택하세요:",
    [
        "우리반 네비게이터",
        "우리반 기본 시간표",
        "이동 수업 및 교실 공지",
        "네비게이션 길 안내",
        "교실 및 특별실 상세정보",
    ],
)

st.markdown(
    "<h1 class='main-title'>🏫 우리반 네비게이터</h1>", unsafe_allow_html=True
)
st.info(
    f"🔔 **알림**: 등록된 교실 변경 사항이 **{len(st.session_state.announcements)}건** 있습니다."
)
st.markdown("---")

if menu == "우리반 네비게이터":
    st.subheader("📋 앱 소개 및 가이드 안내")
    st.markdown(
        """
    <div class="custom-card-blue">
        <h3 style="margin-top:0;">❓ 어느 날 시간표가 갑자기 바뀌거나 특별실 위치가 바뀌어 당황하신 적이 있나요?</h3>
        <h4 style="color:#2563eb; margin-bottom:0;">👉 이제 걱정할 필요 없습니다! '우리반 네비게이터'가 정확하게 안내해 드립니다!</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """<div class="custom-card"><h4>📅 1. 우리반 기본 시간표</h4><p>정규 수업 및 기본 교실 위치 안내</p></div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="custom-card"><h4>📢 2. 이동 수업 및 교실 공지</h4><p>바뀐 이동 수업 장소 확인/등록</p></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """<div class="custom-card"><h4>🗺️ 3. 네비게이션 길 안내</h4><p>특별실까지의 최적 경로 안내</p></div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="custom-card"><h4>🔍 4. 교실 및 특별실 상세정보</h4><p>교실/특별실 위치 및 이용 수칙 안내</p></div>""",
            unsafe_allow_html=True,
        )

elif menu == "우리반 기본 시간표":
    st.subheader("📅 우리반 기본 시간표")
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    today_num = datetime.datetime.now().weekday()
    default_day = weekdays[today_num] if today_num < 5 else "월요일"
    selected_day = st.selectbox(
        "요일 선택:", weekdays, index=weekdays.index(default_day)
    )
    df = pd.DataFrame(
        TIMETABLE[selected_day],
        columns=["교시", "과목", "담당교사", "기본 장소", "준비물"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "이동 수업 및 교실 공지":
    st.subheader("📢 이동 수업 및 교실 공지")
    with st.expander("➕ 새 이동 수업 공지 등록하기"):
        with st.form("add_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                input_date = st.date_input("날짜", value=datetime.date.today())
                input_period = st.selectbox(
                    "교시",
                    [
                        "1교시",
                        "2교시",
                        "3교시",
                        "4교시",
                        "5교시",
                        "6교시",
                        "7교시",
                    ],
                )
                input_subject = st.text_input("과목명")
            with col2:
                input_orig = st.text_input("기존 장소")
                input_changed = st.text_input("변경 장소")
                input_note = st.text_input("비고")
            if st.form_submit_button("공지 등록"):
                if input_subject and input_changed:
                    st.session_state.announcements.append(
                        {
                            "id": len(st.session_state.announcements) + 1,
                            "date": str(input_date),
                            "period": input_period,
                            "subject": input_subject,
                            "original": input_orig or "기존 교실",
                            "changed": input_changed,
                            "note": input_note or "-",
                        }
                    )
                    st.success("등록 완료!")
                    st.rerun()

    for item in reversed(st.session_state.announcements):
        st.markdown(
            f"""
        <div class="notice-card">
            <h4 style="margin-top:0;">[{item['date']}] {item['period']} - {item['subject']}</h4>
            <p>📍 <b>장소:</b> {item['original']} ➡️ <b style="color:#dc2626;">{item['changed']}</b></p>
            <p>📝 <b>비고:</b> {item['note']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

elif menu == "네비게이션 길 안내":
    st.subheader("🗺️ 네비게이션 길 안내")
    col1, col2 = st.columns(2)
    with col1:
        start_point = st.selectbox(
            "출발지:", ["12반 교실 (본관 2층)", "운동장", "본관 입구"]
        )
    with col2:
        dest_point = st.selectbox("도착지 (목적지):", list(ROOM_INFO.keys()))

    if st.button("🚩 경로 안내 시작", type="primary"):
        info = ROOM_INFO[dest_point]
        st.markdown(
            f"""
        <div class="custom-card">
            <h3>🎯 목적지: {dest_point} ({info['location']})</h3>
            <p>🚶 <b>이동 경로:</b> {info['guide']}</p>
            <p>💡 <b>주의 사항:</b> {info['note']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

elif menu == "교실 및 특별실 상세정보":
    st.subheader("🔍 교실 및 특별실 상세정보 사전")
    selected_room = st.selectbox(
        "궁금한 특별실을 선택하세요:", list(ROOM_INFO.keys())
    )
    if selected_room:
        data = ROOM_INFO[selected_room]
        st.markdown(
            f"""
        <div class="custom-card">
            <h3 style="margin-top:0;">📍 {selected_room}</h3>
            <p><b>• 위치:</b> {data['location']}</p>
            <p><b>• 찾아가는 길:</b> {data['guide']}</p>
            <p><b>• 보유 장비/시설:</b> {data['equipment']}</p>
            <p><b>• 담당 교사:</b> {data['teacher']}</p>
            <p><b>• 이용 수칙:</b> <span style="color:#dc2626;">{data['note']}</span></p>
        </div>
        """,
            unsafe_allow_html=True,
        )
