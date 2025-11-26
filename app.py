import streamlit as st
import pandas as pd

# 1. 페이지 설정 (레이아웃을 'wide'로 해서 화면을 넓게 씀)
st.set_page_config(
    page_title="BitConverter",
    page_icon="⚡",
    layout="wide"
)

# 2. 스타일 꾸미기 (커스텀 CSS) - 제목 폰트나 여백 조정
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%; /* 버튼을 꽉 차게 */
        border-radius: 10px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 디자인
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083213.png", width=80)
with col2:
    st.title("BitConverter")
    st.caption("High Performance Text-to-Binary Processor")

st.divider() # 구분선

# 4. 메인 기능 탭
tab1, tab2 = st.tabs(["🔠 ENCODER (변환)", "🔢 DECODER (해석)"])

# --- TAB 1: 인코딩 (텍스트 -> 코드) ---
with tab1:
    # 레이아웃: 입력창(좌) -> 결과창(우)
    col_input, col_result = st.columns([1, 1])

    with col_input:
        st.subheader("Input Text")
        user_input = st.text_area("텍스트를 입력하세요", height=200, placeholder="Hello World")
        
        # 버튼 (primary 타입으로 색상 강조)
        if st.button("🚀 Convert to Code", type="primary", key="btn_encode"):
            if user_input:
                # 변환 로직
                ascii_list = [str(ord(c)) for c in user_input]
                binary_list = [format(ord(c), 'b') for c in user_input]
                
                # 세션 상태에 결과 저장 (새로고침 방지용)
                st.session_state['result_ascii'] = " ".join(ascii_list)
                st.session_state['result_binary'] = " ".join(binary_list)
                st.session_state['input_len'] = len(user_input)
                st.session_state['bit_len'] = sum(len(b) for b in binary_list)
                st.session_state['has_result'] = True
            else:
                st.warning("텍스트를 입력해주세요.")

    with col_result:
        st.subheader("Processing Result")
        
        if st.session_state.get('has_result'):
            # 1. 통계 메트릭 보여주기 (있어 보이는 요소)
            m1, m2 = st.columns(2)
            m1.metric("Characters", f"{st.session_state['input_len']} 자")
            m2.metric("Total Bits", f"{st.session_state['bit_len']} bits")
            
            # 2. 결과 보여주기 (탭으로 구분)
            res_tab1, res_tab2 = st.tabs(["DECIMAL (10진수)", "BINARY (2진수)"])
            
            with res_tab1:
                st.code(st.session_state['result_ascii'], language="text")
            with res_tab2:
                st.code(st.session_state['result_binary'], language="bash")
                
            st.success("Transformation Complete.")
        else:
            st.info("좌측에 텍스트를 입력하고 버튼을 눌러주세요.")

# --- TAB 2: 디코딩 (코드 -> 텍
