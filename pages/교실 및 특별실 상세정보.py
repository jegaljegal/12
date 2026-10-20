import os
import streamlit as st

st.set_page_config(
    page_title="교실 및 특별실 상세정보 & AI",
    page_icon="🔍",
    layout="wide",
)
st.title("🔍 교실 및 특별실 상세정보 사전")

# Gemini AI 설정
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

ROOM_INFO = {
    "제1과학실": {
        "location": "본관 3층 중앙 (302호 옆)",
        "equipment": "현미경, 알코올램프, 실험대, 환기장치",
        "teacher": "주민지 선생님",
        "note": "실습 도구 사용 주의, 음료 및 음식물 반입 금지",
    },
    "제2과학실": {
        "location": "창의관 3층 동쪽 끝",
        "equipment": "화학 실험대, 안전 시약장, 긴급 세안기",
        "teacher": "유우석 선생님",
        "note": "실험복 착용 필수, 실험 중 자리 이탈 금지",
    },
    "음악실": {
        "location": "예술관 2층 정면",
        "equipment": "그랜드 피아노, 각종 타악기, 앰프 시스템",
        "teacher": "김현희 선생님",
        "note": "실내화 필수 착용, 악기 무단 조작 금지",
    },
    "미술실": {
        "location": "예술관 1층 복도 끝",
        "equipment": "이젤, 물감 세척대, 석고상, 작업대",
        "teacher": "유제은 선생님",
        "note": "앞치마 착용 권장, 물 사용 후 개수대 청소 필수",
    },
    "컴퓨터실": {
        "location": "창의관 2층 201호",
        "equipment": "최신 PC 40대, 빔프로젝터, 프린터",
        "teacher": "김미나 선생님",
        "note": "음식물 반입 금지, 착석 후 PC 점검 필수",
    },
    "체육관 (강당)": {
        "location": "운동장 우측 체육관 전용 건물",
        "equipment": "농구대, 배드민턴 네트, 매트, 방송실",
        "teacher": "이학용 선생님",
        "note": "체육화(깨끗한 운동화) 필수 착용",
    },
}

selected_room = st.selectbox(
    "조회할 특별실을 선택하세요:", list(ROOM_INFO.keys())
)
if selected_room:
    data = ROOM_INFO[selected_room]
    st.info(
        f"📍 **위치**: {data['location']}\n\n"
        f"🛠️ **장비/시설**: {data['equipment']}\n\n"
        f"👨‍🏫 **담당 교사**: {data['teacher']}\n\n"
        f"⚠️ **이용 수칙**: {data['note']}"
    )

st.markdown("---")
st.subheader("🤖 AI 네비게이터에게 질문하기 (Gemini)")
user_query = st.text_input(
    "질문을 입력하세요:",
    placeholder="예: 제2과학실 갈 때 실습복 어디서 갈아입어?",
)

if st.button("✨ 질문하기", type="primary"):
    if user_query:
        if ai_client is not None:
            with st.spinner("AI 답변 생성 중..."):
                try:
                    prompt = f"당신은 친절한 학교 길안내 도우미입니다. 질문에 답변하세요: {user_query}"
                    response = ai_client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=prompt
                    )
                    st.write("🤖 **AI 답변:**")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"오류: {e}")
        else:
            st.warning(
                "🔑 GEMINI_API_KEY가 설정되지 않아 기본 안내 모드로 동작합니다."
            )
            st.info(
                "안내: [학교 지도 및 길 안내] 메뉴에서 출발지와 목적지를 선택하시면 경로를 바로 확인하실 수 있습니다!"
            )
    else:
        st.warning("질문을 입력해 주세요.")
