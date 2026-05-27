import streamlit as st
import google.generativeai as genai

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="공부 챗봇",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Gemini 공부 챗봇")

# ---------------------------
# API KEY 불러오기
# ---------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

except Exception:
    st.error("API 키를 불러오지 못했습니다. secrets.toml을 확인하세요.")
    st.stop()

# ---------------------------
# 모델 설정
# ---------------------------
try:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

except Exception as e:
    st.error(f"모델 초기화 오류: {e}")
    st.stop()

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 📚\n"
                "공부를 도와주는 Gemini 챗봇입니다.\n"
                "궁금한 내용을 질문해보세요!"
            )
        }
    ]

# ---------------------------
# 기존 채팅 출력
# ---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# 사용자 입력
# ---------------------------
user_input = st.chat_input("질문을 입력하세요")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 대화 기록 변환
                history = []

                for msg in st.session_state.messages[:-1]:
                    role = "model" if msg["role"] == "assistant" else "user"

                    history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

                # 채팅 세션 시작
                chat = model.start_chat(history=history)

                # 현재 질문 전송
                response = chat.send_message(user_input)

                bot_reply = response.text

                st.markdown(bot_reply)

                # 응답 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_reply
                    }
                )

            except Exception as e:
                error_message = f"오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )

# ---------------------------
# 사이드바
# ---------------------------
with st.sidebar:
    st.header("⚙️ 설정")

    st.info(
        "현재 모델:\n"
        "gemini-2.5-flash-lite"
    )

    if st.button("채팅 기록 삭제"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "채팅 기록이 초기화되었습니다!"
            }
        ]
        st.rerun()
