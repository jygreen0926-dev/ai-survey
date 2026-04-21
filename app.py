import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 1. 운영진 정보 설정 (이메일 주소만 실제 주소로 바꿔주세요!) ---
ADMIN_LIST = {
    "유미짱": "Yoomic663@gmail.com",  # 유미짱님의 실제 이메일로 수정
    "제제야": "jygreen0926@gmail.com"     # 제제야님의 실제 이메일로 수정
}

# 페이지 설정
st.set_page_config(page_title="AI 모임 리서치", layout="centered")

# URL에서 누가 보낸 링크인지 확인하는 기능
query_params = st.query_params
default_admin = query_params.get("admin", "유미짱") # 기본값은 유미짱

# --- 2. UI 부분 ---
st.title("🚀 AI 모임 리서치 앱")
st.write("반갑습니다! 설문을 작성해 주시면 담당 운영진에게 즉시 전달됩니다.")

# 담당 운영진 선택 (링크에 따라 자동으로 유미짱 또는 제제야가 선택됨)
selected_admin = st.selectbox(
    "담당 운영진", 
    options=list(ADMIN_LIST.keys()),
    index=list(ADMIN_LIST.keys()).index(default_admin) if default_admin in ADMIN_LIST else 0
)

name = st.text_input("성함")
ability = st.radio("AI 역량", ["입문자", "초보자", "숙련자", "전문가"])
goals = st.multiselect("참여 목적", ["유튜브", "친목", "자기계발", "사업 활용"])
details = st.text_area("상세 목표")

def send_email(name, ability, goals, details, target_email):
    try:
        # Streamlit Secrets에서 공통 발송 계정 정보 가져오기
        SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
        APP_PASSWORD = st.secrets["APP_PASSWORD"]
        
        # 실제 메일 수신자
        RECEIVER_EMAIL = target_email

        subject = f"[AI 모임] {name}님의 참여 신청서 (담당: {selected_admin})"
        body = f"""
        새로운 설문 응답이 도착했습니다!
        
        [담당 운영진: {selected_admin}]
        1. 성함: {name}
        2. 역량: {ability}
        3. 목적: {", ".join(goals)}
        4. 상세내용: {details}
        """
        
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        return True
    except Exception as e:
        st.error(f"메일 발송 실패: {e}")
        return False

if st.button("설문 제출 및 이메일 전송"):
    if name and goals:
        with st.spinner(f'{selected_admin}님에게 메일을 보내는 중...'):
            target_addr = ADMIN_LIST[selected_admin]
            success = send_email(name, ability, goals, details, target_addr)
            if success:
                st.success(f"감사합니다, {name}님! {selected_admin}님에게 응답이 전달되었습니다.")
                st.balloons()
    else:
        st.warning("이름과 목적을 입력해 주세요.")