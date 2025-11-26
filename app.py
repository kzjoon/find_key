import streamlit as st
import string

# 페이지 설정
st.set_page_config(page_title="카이사르 암호 실습", page_icon="🏛️")

st.title("🏛️ 카이사르 암호(Caesar Cipher) 실습")
st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    <strong>💡 핵심 원리:</strong> 알파벳을 일정한 거리만큼 밀어서 글자를 바꿉니다.<br>
    고대 로마의 황제 '카이사르'가 군사 비밀을 보낼 때 사용했던 역사적인 암호 방식입니다.
</div>
""", unsafe_allow_html=True)

# --- 1. 암호화 설정 (키 선택) ---
st.subheader("1. 암호 열쇠(Key) 설정")
st.write("알파벳을 옆으로 몇 칸 밀어볼까요? (이 숫자가 바로 암호의 '키'입니다.)")

# 슬라이더로 키 선택 (1~25)
key = st.slider("밀어낼 칸 수 (Shift)", 1, 25, 3)

# 시각적 예시 보여주기
st.info(f"🔑 **설정된 규칙:** 모든 알파벳을 오른쪽으로 **{key}칸** 이동합니다.")

# 변환 예시 시각화
example_text = "ABCDEFG"
shifted_example = ""
for char in example_text:
    shifted_char = chr((ord(char) - 65 + key) % 26 + 65)
    shifted_example += shifted_char

st.code(f"""
원래 글자: {example_text}... (A부터 시작)
변환 글자: {shifted_example}... ({chr(65+key)}부터 시작)
""", language="text")

st.markdown("---")

# --- 2. 실습 하기 ---
st.subheader("2. 직접 암호 만들어보기")

# 텍스트 입력
plain_text = st.text_input("암호로 만들고 싶은 영어 문장을 입력하세요:", "HELLO WORLD")

# 암호화/복호화 함수
def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # 복호화면 반대로 밀어야 함
    if mode == 'decrypt':
        shift = -shift
        
    for char in text:
        if char.isalpha():
            # 대문자/소문자 기준점 확인 (ASCII 코드)
            start = ord('A') if char.isupper() else ord('a')
            # (현재글자 - 기준 + 이동칸) % 26 + 기준
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result += new_char
        else:
            # 알파벳이 아니면(공백, 숫자 등) 그대로 둠
            result += char
    return result

# 결과 계산
encrypted_text = caesar_cipher(plain_text, key, mode='encrypt')

# 화면 분할로 전/후 비교
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📝 원래 문장 (Plain Text)")
    st.success(plain_text)

with col2:
    st.markdown("#### 🔒 암호화된 문장 (Cipher Text)")
    st.error(encrypted_text)

st.markdown("---")

# --- 3. 해독 해보기 (복호화) ---
st.subheader("3. 암호 해독하기 (복호화)")
st.write("받은 암호문을 다시 원래대로 돌리려면 어떻게 해야 할까요?")

if st.button("열쇠를 반대로 돌려 해독하기 🔓"):
    decrypted_text = caesar_cipher(encrypted_text, key, mode='decrypt')
    st.balloons()
    st.markdown(f"""
    <div style='padding: 15px; border: 2px solid #4CAF50; border-radius: 10px; text-align: center;'>
        <h3>해독 성공! 🎉</h3>
        <p>암호문 <strong>"{encrypted_text}"</strong> → 키를 <strong>-{key}</strong>만큼 돌림 → 원문 <strong>"{decrypted_text}"</strong></p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. 생기부용 이론 설명 (이건 꼭 넣으세요!) ---
st.markdown("---")
with st.expander("📚 [생기부/세특용] 수학적 원리 보기 (Modulo 연산)"):
    st.markdown(f"""
    ### 1. 순환의 원리 (Modulo)
    이 프로그램은 단순히 더하기만 하는 것이 아니라, **나머지 연산(Modulo, %)**을 사용합니다.
    
    알파벳은 총 26글자이므로, Z(25번째)를 넘어가면 다시 A(0번째)로 돌아와야 합니다.
    이것은 마치 **시계가 12시 다음 1시가 되는 원리**와 같습니다.
    
    ### 2. 수학 공식
    수학적으로 표현하면 다음과 같습니다. ($x$는 알파벳 번호, $n$은 키 값)
    
    $$ f(x) = (x + n) \pmod{{26}} $$
    
    이 간단한 공식이 **컴퓨터 보안(Cryptography)**의 시초가 되었습니다.
    """)
