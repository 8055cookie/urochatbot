
import streamlit as st
import openai

st.set_page_config(page_title="병원 전화상담 챗봇", page_icon="📞")

st.title("🏥 병원 전화상담 챗봇")
st.markdown("비뇨의학과 외래 전화상담 질문을 입력해보세요.")

openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")

# 미리 정의된 FAQ
faq_examples = {
    "슬라이드 어떻게 준비해요?": "암 진단이 나온 경우, 염색된 슬라이드 2장을 준비해주세요.",
    "처방 먼저 해주세요.": "해당 항목은 진료 후 담당 의료진의 판단에 따라 처방됩니다.",
    "검사 거절했는데 다시 하고 싶어요.": "진료 후 다시 의료진에게 요청하시면 처방 가능합니다.",
    "간도 같이 봐주세요.": "영상 검사 결과에서 해당 부위가 확인되면 판독 시 코멘트가 추가됩니다."
}

user_input = st.text_input("🙋 사용자 질문을 입력하세요")

if st.button("응답 받기") and user_input:
    # 사전 응답 우선
    matched = None
    for key in faq_examples:
        if key in user_input:
            matched = faq_examples[key]
            break

    if matched:
        st.success("🤖 챗봇 응답: " + matched)
    elif not openai_api_key:
        st.warning("⚠️ OpenAI API 키를 입력해주세요.")
    else:
        # GPT fallback
        with st.spinner("ChatGPT에게 물어보는 중..."):
            try:
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "넌 병원 전화상담 전용 챗봇이야. 간결하고 친절하게 안내해."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("🤖 챗봇 응답: " + answer)
            except Exception as e:
                st.error(f"API 오류 발생: {str(e)}")
