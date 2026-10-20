import datetime
import streamlit as st

st.set_page_config(
    page_title="이동 수업 및 교실 공지", page_icon="📢", layout="wide"
)
st.title("📢 이동 수업 및 교실 공지 게시판")

# 세션 데이터 초기화
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        {
            "id": 1,
            "date": "2026-10-21",
            "period": "3교시",
            "subject": "과학",
            "teacher": "김과학 선생님",
            "original": "1반 교실",
            "changed": "제2과학실 (창의관 3층)",
            "note": "실험복 착용 필수 및 보안경 지참",
        },
        {
            "id": 2,
            "date": "2026-10-22",
            "period": "5교시",
            "subject": "체육",
            "teacher": "이체육 선생님",
            "original": "운동장",
            "changed": "체육관 (강당)",
            "note": "우천으로 인한 장소 변경",
        },
    ]

# 공지 등록 폼
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
            input_subject = st.text_input("과목명", placeholder="예: 과학")
            input_teacher = st.text_input(
                "담당 선생님", placeholder="예: 김과학 선생님"
            )
        with col2:
            input_orig = st.text_input("기존 장소", placeholder="예: 1반 교실")
            input_changed = st.text_input(
                "변경 장소", placeholder="예: 제2과학실"
            )
            input_note = st.text_input(
                "비고", placeholder="예: 실험복 지참"
            )

        if st.form_submit_button("📢 공지 등록"):
            if input_subject and input_changed:
                st.session_state.announcements.append(
                    {
                        "id": len(st.session_state.announcements) + 1,
                        "date": str(input_date),
                        "period": input_period,
                        "subject": input_subject,
                        "teacher": input_teacher or "담당 교사",
                        "original": input_orig or "기존 교실",
                        "changed": input_changed,
                        "note": input_note or "-",
                    }
                )
                st.success("새로운 공지가 성공적으로 등록되었습니다!")
                st.rerun()
            else:
                st.error("과목명과 변경 장소는 필수 입력 사항입니다.")

st.write("### 🚨 등록된 장소 변경 공지 목록")

# .get()을 사용해 이전 데이터에 teacher 키가 없어도 에러가 나지 않도록 예외 처리
for item in reversed(st.session_state.announcements):
    teacher_info = item.get("teacher", "담당 교사")
    date_info = item.get("date", "")
    period_info = item.get("period", "")
    subject_info = item.get("subject", "")
    orig_info = item.get("original", "기존 교실")
    changed_info = item.get("changed", "")
    note_info = item.get("note", "-")

    st.warning(
        f"**[{date_info}] {period_info} - {subject_info} ({teacher_info})**\n\n"
        f"📍 **위치 변경**: {orig_info} ➡️ **{changed_info}**\n\n"
        f"📝 **비고**: {note_info}"
    )
