import streamlit as st
from openai import OpenAI
import time

# ==========================================
# 👇 GitHub 버전은 API 키를 코드에 직접 안 씁니다!
# (나중에 Streamlit 설정 화면에서 따로 넣을 겁니다)
# ==========================================
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("🚨 API 키가 설정되지 않았습니다! Streamlit Secrets를 확인하세요.")
    st.stop()
# ==========================================

# 1. 페이지 설정
st.set_page_config(page_title="점성술사의 매직 8볼", page_icon="🎱", layout="centered")

# 2. CSS 디자인 (원형 창 + 짧은 텍스트 최적화)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700&family=Black+Han+Sans&display=swap');
    
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=2071&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
        font-family: 'Nanum Myeongjo', serif;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.4); z-index: 0; pointer-events: none;
    }
    .main-title {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(to right, #a8c0ff, #d9a7c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        margin-top: 20px;
        position: relative; z-index: 1;
    }
    .sub-title {
        text-align: center; color: #ddd; margin-bottom: 30px; font-size: 1.1rem; position: relative; z-index: 1;
    }
    div[data-testid="stTextInput"] > div > div > input {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px; padding: 15px; font-size: 1.2rem;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        font-family: 'Black Han Sans', sans-serif;
        font-size: 1.2rem;
        padding: 12px 30px;
        border: none;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        transition: 0.3s;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(168, 192, 255, 0.8);
    }
    .magic-ball-container {
        width: 350px; height: 350px;
        margin: 60px auto;
        position: relative;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #444, #000);
        box-shadow: inset -10px -10px 30px rgba(255,255,255,0.1), 0 20px 60px rgba(0,0,0,0.9);
        animation: floatBall 6s ease-in-out infinite;
        z-index: 1;
    }
    .circle-display {
        width: 170px; height: 170px;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, #0066ff, #001233);
        box-shadow: 0 0 40px #0066ff, inset 0 0 20px #000;
        display: flex; align-items: center; justify-content: center;
        padding: 10px;
    }
    .magic-text {
        font-family: 'Black Han Sans', sans-serif;
        color: #e0f7fa;
        font-size: 1.5rem;
        text-align: center;
        line-height: 1.2;
        text-shadow: 0 0 10px #fff;
        width: 100%;
        word-break: keep-all;
        animation: fadeIn 0.5s ease-out;
    }
    @keyframes floatBall { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

client = OpenAI(api_key=api_key)

def get_oracle_response(question):
    system_prompt = """
    너는 '매직 8볼'이다. 질문에 대해 결론만 딱 잘라 말해라.
    [규칙] 1. 길이: 10자 이내. 2. 말투: 반말. 단답형. 재치 있게.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception:
        return "신호 약함."

st.markdown("<h1 class='main-title'>✨ 점성술사의 매직 8볼 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>짧고 굵게 운명을 알려주마.</p>", unsafe_allow_html=True)

question = st.text_input("질문", placeholder="예: 오늘 야식 참을까?", label_visibility="collapsed")
if 'answer' not in st.session_state: st.session_state['answer'] = "질문해."

if st.button("🔮 운명 확인하기 (Click)"):
    if not question: st.warning("질문 안 하냐?")
    else:
        with st.spinner("..."):
            time.sleep(0.8)
            st.session_state['answer'] = get_oracle_response(question)

st.markdown(f"""<div class="magic-ball-container"><div class="circle-display"><div class="magic-text">{st.session_state['answer']}</div></div></div>""", unsafe_allow_html=True)
