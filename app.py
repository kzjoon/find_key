import streamlit as st
import math

# 페이지 설정
st.set_page_config(
    page_title="RSA 암호화 원리 탐구",
    page_icon="🔐",
    layout="centered"
)

# --- 유틸리티 함수 (수학 계산) ---

def gcd(a, b):
    """최대공약수 계산 (유클리드 호제법)"""
    while b:
        a, b = b, a % b
    return a

def find_e(phi):
    """공개키 e 구하기: 1 < e < phi 이며, phi와 서로소인 가장 작은 수"""
    for e in range(3, phi):
        if gcd(e, phi) == 1:
            return e
    return None

def find_d(e, phi):
    """개인키 d 구하기: (d * e) % phi == 1 인 d 찾기 (확장 유클리드 대신 이해 쉬운 반복문 사용)"""
    d = 2
    while True:
        if (d * e) % phi == 1:
            return d
        d += 1
        # 무한 루프 방지 (작은 수 범위 내에서 실습하므로 안전장치)
        if d > 100000: 
            return None

# --- UI 디자인 ---

st.title("🔐 RSA 암호화 알고리즘 탐구")
st.markdown("""
<div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    <strong>학습 목표:</strong> 현대 정보 보안의 핵심인 <strong>RSA 공개키 암호화</strong> 과정을 
    수학적 원리(소수와 나머지 연산)를 통해 단계별로 시뮬레이션하고 이해합니다.
</div>
""", unsafe_allow_html=True)

# 1. 소수 선택 단계
st.header("1단계: 두 개의 소수($p, q$) 선택")
st.markdown("암호화를 위한 두 개의 작은 소수를 선택합니다. (실제 RSA는 아주 큰 소수를 사용합니다.)")

col1, col2 = st.columns(2)
with col1:
    p = st.selectbox("첫 번째 소수 ($p$)", [2, 3, 5, 7, 11, 13, 17, 19, 23])
with col2:
    q = st.selectbox("두 번째 소수 ($q$)", [3, 5, 7, 11, 13, 17, 19, 23, 29], index=2)

if p == q:
    st.error("⚠️ 서로 다른 두 소수를 선택해야 보안성이 성립합니다.")
    st.stop()

# 2. 키 생성 단계
st.markdown("---")
st.header("2단계: 공개키와 개인키 생성")

# N과 Phi 계산
n = p * q
phi = (p - 1) * (q - 1)

# e와 d 계산
e = find_e(phi)
d = find_d(e, phi)

st.latex(r"1. \quad N = p \times q = " + f"{p} \\times {q} = {n}")
st.latex(r"2. \quad \phi(N) = (p-1)(q-1) = " + f"{p-1} \\times {q-1} = {phi}")
st.latex(r"3. \quad \text{공개키 } e \text{ (phi와 서로소)}: " + f"{e}")
st.latex(r"4. \quad \text{개인키 } d \text{ (} e \times d \pmod{\phi(N)} = 1 \text{)}: " + f"{d}")

st.info(f"""
💡 **결과 키 세트**
* **🔓 공개키(Public Key):** 누구나 알 수 있는 키 👉 ($N={n}, e={e}$)
* **🔑 개인키(Private Key):** 나만 알고 있어야 하는 키 👉 ($N={n}, d={d}$)
""")

# 3. 암호화 단계
st.markdown("---")
st.header("3단계: 메시지 암호화 (Encryption)")
st.markdown("보내고 싶은 숫자를 입력하면 **공개키**를 이용해 암호문으로 바꿉니다.")

# 메시지 입력 (N보다 작아야 함)
max_msg = n - 1
message = st.number_input(f"전송할 숫자 메시지 (1 ~ {max_msg} 사이의 정수)", min_value=1, max_value=max_msg, value=12)

# 암호화 공식: C = M^e mod N
encrypted_msg = pow(message, e, n)

st.markdown(f"**암호화 공식:** $C = M^e \pmod N$")
st.latex(f"C = {message}^{{{e}}} \pmod{{{n}}}")
st.success(f"🔒 암호화된 결과값(Ciphertext): **{encrypted_msg}**")
st.caption(f"설명: {message}를 {e}번 곱한 뒤, {n}으로 나눈 나머지가 {encrypted_msg}입니다.")


# 4. 복호화 단계
st.markdown("---")
st.header("4단계: 메시지 복호화 (Decryption)")
st.markdown("받은 암호문을 **개인키**를 이용해 원래의 숫자로 되돌립니다.")

if st.button("암호문 해독하기 🔓"):
    # 복호화 공식: M = C^d mod N
    decrypted_msg = pow(encrypted_msg, d, n)
    
    st.markdown(f"**복호화 공식:** $M = C^d \pmod N$")
    st.latex(f"M = {encrypted_msg}^{{{d}}} \pmod{{{n}}}")
    
    if decrypted_msg == message:
        st.success(f"🎉 복호화 성공! 원래 메시지: **{decrypted_msg}**")
        st.balloons()
    else:
        st.error("복호화 실패... 뭔가 잘못되었습니다.")
