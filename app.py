import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 1. 운영진 정보 (수신 이메일) ---
ADMIN_LIST = {
    "유미짱": "Yoomic663@gmail.com", 
    "제제": "jygreen0926@gmail.com"
}

# 페이지 설정
st.set_page_config(page_title="AI 모임 리서치", layout="centered")

# URL 파라미터로 운영진 자동 선택
query_params = st.query_params
default_admin = query_params.get("admin", "유미짱")

# --- 2. UI 및 설문 구성 ---
st.title("🚀 AI 모임 리서치 앱")
st.info("**[안내]** 작성하신 내용은 선택하신 담당 운영진에게 즉시 전달됩니다.")

selected_admin = st.selectbox(
    "담당 운영진을 확인해 주세요", 
    options=list(ADMIN_LIST.keys()),
    index=list(ADMIN_LIST.keys()).index(default_admin) if default_admin in ADMIN_LIST else 0
)

name = st.text_input("성함")
phone = st.text_input("연락처")
ability = st.radio("AI 역량", ["입문자", "초보자", "숙련자", "전문가"])
goals = st.multiselect("참여 목적", ["유튜브", "친목", "자기계발", "사업 활용"])
details = st.text_area("상세 목표")
privacy_agree = st.checkbox("개인정보 수집 및 이용에 동의합니다.")

# --- 3. 이메일 발송 함수 (Secrets만 참조) ---
def send_email(name, phone, ability, goals, details, target_email):
    try:
        # 이 부분에서 제제님의 Secrets 정보를 가져옵니다.
        S_EMAIL = st.secrets["SENDER_EMAIL"]
        S_PASS = st.secrets["APP_PASSWORD"]
        
        subject = f"[AI 모임] {name}님의 참여 신청서 (담당: {selected_admin})"
        body = f"""
        새로운 신청서가 도착했습니다.
        
        - 담당 운영진: {selected_admin}
        - 성함: {name}
        - 연락처: {phone}
        - 역량: {ability}
        - 목적: {', '.join(goals)}
        - 상세내용: {details}
        """
        
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = S_EMAIL
        msg['To'] = target_email # 유미짱 혹은 제제님 메일로 발송

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(S_EMAIL, S_PASS)
            server.sendmail(S_EMAIL, target_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"메일 발송 실패: {e}")
        return False

# --- 4. 제출 버튼 로직 ---
if st.button("설문 제출하기"):
    if not privacy_agree:
        st.warning("개인정보 동의가 필요합니다.")
    elif name and phone and goals:
        with st.spinner('운영진에게 전송 중입니다...'):
            success = send_email(name, phone, ability, goals, details, ADMIN_LIST[selected_admin])
            if success:
                st.success(f"전송 완료! {selected_admin}님이 곧 연락드릴 예정입니다.")
                st.balloons()
    else:
        st.warning("필수 항목(성함, 연락처, 목적)을 모두 입력해 주세요.")