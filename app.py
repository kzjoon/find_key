import streamlit as st

# 사이트 기본 설정
st.set_page_config(page_title="컴퓨터 통역기", page_icon="💻")

st.title("💻 컴퓨터 통역기 (Text Converter)")
st.write("컴퓨터는 0과 1밖에 모릅니다. 우리가 쓰는 글자가 컴퓨터 내부에서 어떻게 변하는지 확인해보세요!")

# 탭을 나누어 기능 분리 (변환하기 vs 되돌리기)
tab1, tab2 = st.tabs(["🔤 텍스트 ➡ 코드(분해)", "🔢 코드 ➡ 텍스트(조립)"])

# --- 기능 1: 텍스트를 코드로 변환 (인코딩) ---
with tab1:
    st.subheader("사람의 말을 컴퓨터 언어로 변환")
    user_input = st.text_input("변환할 문장을 입력하세요 (예: Hello, 내 이름은...)", "Hello")

    if user_input:
        # 결과를 저장할 리스트들
        ascii_list = []
        binary_list = []

        # 한 글자씩 반복하며 변환
        for char in user_input:
            code_num = ord(char)  # 문자를 아스키/유니코드 숫자로 변환
            binary_num = format(code_num, 'b')  # 숫자를 이진수로 변환
            
            ascii_list.append(str(code_num))
            binary_list.append(binary_num)

        # 결과 보여주기
        st.success("변환 완료!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🔢 10진수 (ASCII/Unicode)")
            # 리스트를 공백으로 합쳐서 보여줌
            st.code(" ".join(ascii_list))
            st.caption("컴퓨터 주소값(십진수)입니다.")

        with col2:
            st.warning("👾 2진수 (Binary)")
            st.code(" ".join(binary_list))
            st.caption("실제 컴퓨터 메모리에 저장되는 형태(0과 1)입니다.")

        # 상세 분석 (표 형태)
        with st.expander("🔍 한 글자씩 상세히 보기"):
            data = {
                "글자": list(user_input),
                "10진수": ascii_list,
                "2진수": binary_list
            }
            st.table(data)

# --- 기능 2: 코드를 텍스트로 변환 (디코딩) ---
with tab2:
    st.subheader("컴퓨터 언어를 사람의 말로 해석")
    st.write("위에서 얻은 **10진수 숫자**들을 **공백(스페이스바)**으로 띄워서 입력해주세요.")
    
    code_input = st.text_area("숫자 코드 입력 (예: 72 101 108 108 111)", "72 101 108 108 111")

    if st.button("해석하기 (Decode)"):
        try:
            # 입력된 문자열을 공백 기준으로 자르기
            num_strings = code_input.split()
            
            decoded_chars = []
            for num_str in num_strings:
                num = int(num_str) # 문자를 숫자로 변환
                char = chr(num)    # 숫자를 다시 글자로 변환
                decoded_chars.append(char)
            
            result_text = "".join(decoded_chars)
            
            st.balloons() # 성공 축하 효과
            st.success(f"해석 결과: {result_text}")
            
        except ValueError:
            st.error("오류! 숫자만 입력해주세요. (글자나 특수문자가 섞여 있는지 확인하세요)")
        except Exception as e:
            st.error(f"알 수 없는 오류가 발생했습니다: {e}")

# --- 사이드바: 원리 설명 (세특용) ---
with st.sidebar:
    st.header("💡 원리 알아보기")
    st.markdown("""
    **1. 인코딩 (Encoding)**
    사람의 문자를 컴퓨터가 이해하는 숫자로 바꾸는 과정입니다.
    파이썬의 `ord()` 함수를 사용했습니다.
    
    **2. 디코딩 (Decoding)**
    저장된 숫자를 다시 화면에 문자로 보여주는 과정입니다.
    파이썬의 `chr()` 함수를 사용했습니다.
    
    **3. 아스키(ASCII) & 유니코드**
    영어는 아스키 코드로, 한글은 유니코드로 변환되어 저장됩니다.
    """)
