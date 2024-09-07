import streamlit as st
import os
import uuid
import json
from urllib import request, parse, error

def send_simple_webhook(msg, webhook_url, model="gpt-4o-mini", session_id=None):
    try:
        # Create the query parameters
        params = {
            'msg': msg,
            'model': model,
            'session_id': session_id
        }
        
        encoded_params = parse.urlencode(params)
        full_url = f"{webhook_url}?{encoded_params}"
        
        req = request.Request(full_url, method='GET')
        with request.urlopen(req, timeout=60) as response:
            return response.read().decode()
    except error.HTTPError as e:
        return f"HTTP Error {e.code}: {e.reason}. Response: {e.read().decode()}"
    except error.URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 메인 함수 정의
def main():
    # 1단계 페이지 레이아웃 설정
    st.set_page_config(layout="wide")
    st.title("AI비서 알프레드")

    # 2단계 Webhook URL 설정
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        with st.sidebar:
            webhook_url = st.text_input("n8n webhook url", key="webhook_url")



    # 3단계states 정의
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Initialize session_id if not present
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())


    # 채팅 메시지 표시
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    ## 채팅
    prompt = st.chat_input("무엇이 궁금한가요?")
    if prompt:

        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # 웹훅 호출 및 응답 처리
        with st.chat_message("assistant"):
            response = send_simple_webhook(prompt, webhook_url, model="gpt-4o-mini", session_id=st.session_state.session_id)
            st.markdown(response)
        # 어시스턴트 메시지 추가
        st.session_state.messages.append({"role": "assistant", "content": response})


# 메인 함수 실행
if __name__ == "__main__":
    main()