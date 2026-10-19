import datetime
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리 반 네비게이터",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Gemini AI 설정 (선택적 사용 / 예외 처리 포함)
ai_client = None
try:
    from google import genai

    # Secrets 및 환경변수 확인
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        ai_client = genai.Client(api_key=api_key)
except Exception:
    ai_client = None

# 3. Session State 데이터 초기화
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        {
            "date": "2026-10-19",
            "period": "3교시",
            "subject": "과학",
            "original": "1반 교실",
            "changed": "제2과학실 (창의관 3층)",
            "note": "실험복 착용 및 창의관 3층으로 이동",
        },
        {
            "date": "2026-10-20",
            "period": "5교시",
            "subject": "체육",
            "original": "운동장",
            "changed": "체육관 (강당)",
            "note": "우천으로 인한 장소 변경",
        },
    ]

# 4. 기본 시간표 및 교실 정보 데이터베이스
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
        "guide": "본관 중앙 계단을 이용해 3층으로 올라가서 오른쪽 두 번째 교실입니다.",
        "note": "실습 도구 주의, 음료 반입 금지",
    },
    "제2과학실": {
        "location": "창의관 3층 끝",
        "guide": "본관 2층 구름다리를 통해 창의관으로 이동 후 3층으로 올라가세요.",
        "note": "실험복 착용 필수",
    },
    "음악실": {
        "location": "예술관 2층",
        "guide": "예술관 입구 우측 계단 이용 후 2층 정면입니다.",
        "note": "실내화 착용, 악기 손대지 않기",
    },
    "미술실": {
        "location": "예술관 1층",
        "guide": "예술관 1층 중앙 통로 우측입니다.",
        "note": "앞치마 준비",
    },
    "컴퓨터실": {
        "location": "창의관 2층",
        "guide": "창의관 엘리베이터 옆 201호입니다.",
        "note": "음식물 반입 절대 금지",
    },
    "체육관 (강당)": {
        "location": "체육관 동 1층",
        "guide": "운동장을 지나 우측 체육관 건물 입구로 들어오세요.",
        "note": "체육화 착용 필수",
    },
    "영어 전용실": {
        "location": "본관 2층 동쪽",
        "guide": "1학년 교실 복도 끝 계단 옆입니다.",
        "note": "교재 지참",
    },
}

# 5. 헤더 화면
st.title("🏫 우리 반 네비게이터")
st.markdown(
    "**오늘의 시간표를 제공하고, 바뀐 교실 및 이동 수업 위치를 당황하지 않고 찾아가도록 안내합니다!**"
)

# 6. 사이드바 메뉴 (기획안 스케치 반영)
st.sidebar.image(
    "https://img.icons8.com/color/96/school.png", use_container_width=False
)
st.sidebar.title("📌 네비게이션 메뉴")

menu = st.sidebar.radio(
    "원하는 서비스를 선택하세요:",
    [
        "📅 우리 반 기본 시간표",
        "📢 이동 수업 및 교실 공지",
        "🗺️ 학교 지도 및 길 안내",
        "🔍 교실/특별실 상세 정보 & AI 길잡이",
    ],
)

# ---------------------------------------------------------
# 메뉴 1: 우리 반 기본 시간표
# ---------------------------------------------------------
if menu == "📅 우리 반 기본 시간표":
    st.subheader("📅 요일별 기본 시간표")

    # 오늘 요일 계산
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    today_num = datetime.datetime.now().weekday()
    default_day = weekdays[today_num] if today_num < 5 else "월요일"

    selected_day = st.selectbox(
        "요일을 선택하세요:",
        ["월요일", "화요일", "수요일", "목요일", "금요일"],
        index=["월요일", "화요일", "수요일", "목요일", "금요일"].index(
            default_day
        ),
    )

    data = TIMETABLE[selected_day]
    df = pd.DataFrame(data, columns=["교시", "과목", "기본 장소"])

    st.write(f"### 📖 {selected_day} 시간표")
    st.table(df)

    st.info(
        "💡 **팁**: 갑작스럽게 장소가 변경된 수업은 [📢 이동 수업 및 교실 공지] 메뉴에서 확인하세요!"
    )

# ---------------------------------------------------------
# 메뉴 2: 이동 수업 및 교실 공지
# ---------------------------------------------------------
elif menu == "📢 이동 수업 및 교실 공지":
    st.subheader("📢 이동 수업 및 장소 변경 공지")

    st.write("시간표 변동이나 장소 변경 사항을 실시간으로 확인하고 등록합니다.")

    # 공지 추가 양식
    with st.expander("➕ 새 이동 수업/장소 변경 공지 등록하기"):
        with st.form("add_notice_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                input_date = st.date_input(
                    "날짜", value=datetime.date.today()
                )
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
                input_subject = st.text_input(
                    "과목명", placeholder="예: 과학"
                )
            with col2:
                input_orig = st.text_input(
                    "기존 장소", placeholder="예: 1반 교실"
                )
                input_changed = st.text_input(
                    "변경 장소", placeholder="예: 제2과학실"
                )
                input_note = st.text_input(
                    "준비물/비고", placeholder="예: 실습복 지참"
                )

            submit_btn = st.form_submit_dict = st.form_submit_button(
                "공지 등록"
            )

            if submit_btn:
                if input_subject and input_changed:
                    st.session_state.announcements.append(
                        {
                            "date": str(input_date),
                            "period": input_period,
                            "subject": input_subject,
                            "original": input_orig or "기존 교실",
                            "changed": input_changed,
                            "note": input_note or "-",
                        }
                    )
                    st.success("새로운 공지가 성공적으로 등록되었습니다!")
                else:
                    st.error("과목명과 변경 장소는 필수 항목입니다.")

    # 공지 목록 표시
    st.write("### 🚨 등록된 장소 변경 알림")
    if st.session_state.announcements:
        for idx, item in enumerate(
            reversed(st.session_state.announcements)
        ):
            st.warning(
                f"**[{item['date']}] {item['period']} - {item['subject']}**\n\n"
                f"📍 **위치 변경**: {item['original']} ➡️ **{item['changed']}**\n\n"
                f"📝 **비고**: {item['note']}"
            )
    else:
        st.info("현재 등록된 장소 변경 공지가 없습니다.")

# ---------------------------------------------------------
# 메뉴 3: 학교 지도 및 길 안내
# ---------------------------------------------------------
elif menu == "🗺️ 학교 지도 및 길 안내":
    st.subheader("🗺️ 학교 건물 및 길 안내")

    st.write("출발지와 도착지를 선택하면 최적 이동 경로를 안내합니다.")

    col1, col2 = st.columns(2)
    with col1:
        start_point = st.selectbox(
            "출발지 선택:", ["1반 교실 (본관 2층)", "운동장", "본관 입구"]
        )
    with col2:
        dest_point = st.selectbox("목적지 선택:", list(ROOM_INFO.keys()))

    if st.button("🚩 경로 안내 시작"):
        info = ROOM_INFO[dest_point]
        st.success(f"🎯 **목적지**: {dest_point} ({info['location']})")
        st.write(f"🚶 **이동 방법**: {info['guide']}")
        st.info(f"💡 **주의 사항**: {info['note']}")

    st.markdown("---")
    st.write("### 🏫 건물 구조 요약")
    st.markdown(
        """
    - **본관**: 1층(행정실/교무실), 2층(1학년 교실/영어실), 3층(2학년 교실/제1과학실), 4층(가정실습실)
    - **창의관**: 2층(컴퓨터실), 3층(제2과학실)
    - **예술관**: 1층(미술실), 2층(음악실)
    - **체육관**: 운동장 우측 건물
    """
    )

# ---------------------------------------------------------
# 메뉴 4: 교실/특별실 상세 정보 & AI 길잡이
# ---------------------------------------------------------
elif menu == "🔍 교실/특별실 상세 정보 & AI 길잡이":
    st.subheader("🔍 교실/특별실 상세 정보 & AI 길잡이")

    # 1. 일반 검색
    st.write("### 📌 특별실 상세 사전")
    selected_room = st.selectbox(
        "정보를 확인할 교실을 선택하세요:", list(ROOM_INFO.keys())
    )

    if selected_room:
        room_data = ROOM_INFO[selected_room]
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("위치", room_data["location"])
        with col_b:
            st.metric("특이사항", room_data["note"])
        st.write(f"**길 안내 상세:** {room_data['guide']}")

    st.markdown("---")

    # 2. Gemini AI 질문하기
    st.write("### 🤖 AI 네비게이터에게 물어보기 (Gemini)")
    st.caption(
        "복잡한 길 찾기나 수업 위치에 대해 자연스럽게 질문해 보세요!"
    )

    user_query = st.text_input(
        "질문을 입력하세요:",
        placeholder="예: 비 오는 날 체육관까지 우산 없이 가는 제일 빠른 길이 있어?",
    )

    if st.button("AI에게 질문하기"):
        if not user_query:
            st.warning("질문을 입력해주세요.")
        else:
            if ai_client is not None:
                with st.spinner("AI 네비게이터가 답변을 생각 중입니다..."):
                    try:
                        prompt = f"""
                        당신은 학교의 길 안내 및 시간표 안내를 도와주는 친절한 '우리 반 네비게이터' AI 도우미입니다.
                        학생이 다음 질문에 대해 명확하고 친절하게 길 안내나 도움을 주도록 답변해 주세요.
                        
                        [학교 기본 구조 정보]
                        - 본관: 1층(행정실), 2층(1학년 교실, 영어실), 3층(2학년 교실, 제1과학실), 4층(가정실)
                        - 창의관: 2층(컴퓨터실), 3층(제2과학실) -> 본관 2층 구름다리로 연결됨
                        - 예술관: 1층(미술실), 2층(음악실)
                        - 체육관: 운동장 우측
                        
                        [학생 질문]: {user_query}
                        """
                        response = ai_client.models.generate_content(
                            model="gemini-2.5-flash-lite", contents=prompt
                        )
                        st.write("🤖 **AI 네비게이터 답변:**")
                        st.info(response.text)
                    except Exception as e:
                        st.error(
                            f"AI 답변 생성 중 오류가 발생했습니다: {e}"
                        )
            else:
                # API 키가 설정되지 않았을 때의 안내 및 기본 모의 응답
                st.warning(
                    "🔑 GEMINI_API_KEY가 설정되지 않아 기본 안내 모드로 작동합니다."
                )
                st.write("🤖 **기본 안내 답변:**")
                st.info(
                    f"'{user_query}'에 대한 안내입니다.\n\n"
                    "교실 위치나 이동 경로는 상단의 **[🗺️ 학교 지도 및 길 안내]** 메뉴에서 도착지별 상세 가이드를 통해 더 빠르고 정확하게 확인하실 수 있습니다!"
                )
