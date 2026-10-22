import datetime
import streamlit as st

st.set_page_config(
    page_title="이동 수업 및 교실 공지", page_icon="📢", layout="wide"
)

st.title("📢 이동 수업 및 교실 공지 게시판")

# Session State 데이터 관리 (김과학 선생님 ➡️ 유우석 선생님으로 변경)
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        {
            "id": 1,
            "date": "2026-10-21",
            "period": "3교시",
            "subject": "과학",
            "teacher": "유우석 선생님",  # 유우석 선생님으로 변경
            "original": "12반 교실",
            "changed": "제2과학실 (창의관 3층)",
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

# 새 이동 수업 공지 등록 폼
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
            input_teacher = st.text_input("선생님 이름")
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
                        "teacher": f"{input_teacher} 선생님"
                        if input_teacher
                        else "담당 선생님",
                        "original": input_orig or "기존 교실",
                        "changed": input_changed,
                        "note": input_note or "-",
                    }
                )
                st.success("등록 완료!")
                st.rerun()

st.subheader("🚨 등록된 장소 변경 공지 목록")

# 공지 카드 목록 출력
for item in reversed(st.session_state.announcements):
    teacher_name = item.get("teacher", "담당 선생님")
    st.warning(
        f"**[{item['date']}] {item['period']} - {item['subject']} ({teacher_name})**\n\n"
        f"📍 **위치 변경:** {item['original']} ➡️ **{item['changed']}**\n\n"
        f"📝 **비고:** {item['note']}"
    )
