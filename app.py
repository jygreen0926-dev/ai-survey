import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 이메일 설정 (본인 정보로 수정하세요) ---
SENDER_EMAIL = "당신의계정@gmail.com"  
APP_PASSWORD = "복사한16자리비밀번호" 
RECEIVER_EMAIL = "받을계정@gmail.com" 

def send_email(name, nickname, user_email, phone, ability, goals, details):
    subject = Header(f"[AI 모임] {name}({nickname})님의 참여 신청서", "utf-8")
    
    # 본문에 새로운 정보들 추가
    body = f"""
    새로운 설문 응답이 도착했습니다.
    
    1. 성함: {name}
    2. 닉네임: {nickname}
    3. 연락처: {phone}
    4. 신청자 이메일: {user_email}
    5. 역량: {ability}
    6. 목적: {", ".join(goals)}
    7. 상세내용: {details}
    
    --- 개인정보 수집 및 활용에 동의함 ---
    """
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg) 
        return True
    except Exception as e:
        st.error(f"메일 발송 실패: {e}")
        return False

# --- UI 부분 ---
st.title("🚀 AI 모임 참여자 역량 조사")
st.write("모임 운영을 위한 소중한 정보를 입력해 주세요.")

# 1. 인적 사항
st.subheader("📋 기본 정보")
col1, col2 = st.columns(2) # 화면을 반으로 나눠서 배치
with col1:
    name = st.text_input("성함")
    nickname = st.text_input("닉네임")
with col2:
    phone = st.text_input("전화번호", placeholder="010-0000-0000")
    user_email = st.text_input("본인 이메일 주소")

# 2. 역량 및 목적
st.subheader("💡 역량 및 목표")
ability = st.radio("현재 AI 및 컴퓨터 활용 역량", ["아예 처음", "몇 번 접해봄", "숙련자", "전문가"])
goals = st.multiselect("AI 모임 참여 목적", ["유튜브 수익", "친목 도모", "자기계발", "사업 활용"])
details = st.text_area("상세한 목표나 하고 싶은 말")

# 3. 개인정보 동의 (중요!)
st.subheader("🔐 개인정보 동의")
agreement_text = """
[개인정보 수집 및 이용 동의]
1. 수집 항목: 성함, 닉네임, 연락처, 이메일 주소
2. 수집 목적: AI 모임 운영 및 안내 연락
3. 보유 기간: 모임 종료 후 1개월 이내 파기
* 귀하는 동의를 거부할 권리가 있으나, 거부 시 모임 참여가 제한될 수 있습니다.
"""
st.info(agreement_text)
agree = st.checkbox("위의 개인정보 수집 및 이용에 동의합니다.")

# 제출 버튼
if st.button("설문 제출 및 이메일 전송"):
    if not agree:
        st.error("개인정보 수집에 동의해 주셔야 제출이 가능합니다.")
    elif name and phone and user_email and goals:
        with st.spinner('이메일을 보내는 중입니다...'):
            success = send_email(name, nickname, user_email, phone, ability, goals, details)
            if success:
                st.success(f"성공! {name}님, 운영진에게 신청서가 안전하게 발송되었습니다.")
    else:
        st.warning("필수 항목(성함, 연락처, 이메일, 목적)을 모두 입력해 주세요.")