import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 1. 운영진 정보 설정 (입력하신 주소로 적용 완료!) ---
ADMIN_LIST = {
    "유미짱": "Yoomic663@gmail.com", 
    "제제": "jygreen0926@gmail.com"
}

# 페이지 설정
st.set_page_config(page_title="AI 모임 리서치", layout="centered")

# URL 파라미터로 운영진 자동 선택 기능
query_params = st.query_params
default_admin = query_params.get("admin", "유미짱")

# --- 2. UI 부분 ---
st.title("🚀 AI 모임 리서치 앱")
st.write("반갑습니다! 아래 내용을 작성해 주시면 담당 운영진에게 전달됩니다.")

# 담당 운영진 선택
selected_admin = st.selectbox(
    "담당 운영진", 
    options=list(ADMIN_LIST.keys()),
    index=list(ADMIN_LIST.keys()).index(default_admin) if default_admin in ADMIN_LIST else 0
)

# 설문 항목들
name = st.text_input("성함")
ability = st.radio("AI 역량", ["입문자", "초보자", "숙련자", "전문가"])
goals = st.multiselect("참여 목적", ["유튜브", "친목", "자기계발", "사업 활용"])
details = st.text_area("상세 목표")

def send_email(name, ability, goals, details, target_email):
    try:
        # Streamlit Secrets에서 발송용 계정 정보 가져오기
        # (Secrets 창에 SENDER_EMAIL과 APP_PASSWORD가 정확히 있어야 합니다!)
        S_EMAIL = st.secrets["SENDER_EMAIL"]
        S_PASS = st.secrets["APP_PASSWORD"]
        
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
        msg['From'] = S_EMAIL
        msg['To'] = target_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(S_EMAIL, S_PASS)
            server.sendmail(S_EMAIL, target_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"메일 발송 실패: {e}")
        return False

# 제출 버튼
if st.button("설문 제출 및 이메일 전송"):
    if name and goals:
        with st.spinner(f'{selected_admin}님에게 전송 중...'):
            target_addr = ADMIN_LIST[selected_admin]
            success = send_email(name, ability, goals, details, target_addr)
            if success:
                st.success(f"감사합니다, {name}님! {selected_admin}님에게 응답이 전달되었습니다.")
                st.balloons()
    else:
        st.warning("이름과 목적을 입력해 주세요.")