import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 1. 운영진 이메일 설정 (수신용) ---
ADMIN_LIST = {
    "유미짱": "Yoomic663@gmail.com",
    "제제": "jygreen0926@gmail.com"
}

# 페이지 설정
st.set_page_config(page_title="AI 모임 리서치", layout="centered")

# URL 파라미터 확인 (운영진 자동 선택용)
query_params = st.query_params
default_admin = query_params.get("admin", "유미짱")

# --- 2. UI 구성 ---
st.title("🚀 AI 모임 리서치 앱")

st.info("""
**[개인정보 수집 및 이용 안내]**
* 수집 항목: 성함, 연락처, AI 역량, 참여 목적 등
* 수집 목적: AI 모임 운영 및 안내 연락
* 보유 기간: 목적 달성 후 즉시 파기
""")

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

# --- 3. 메일 발송 로직 ---
def send_email(name, phone, ability, goals, details, target_email):
    try:
        # Secrets에서 정보 가져오기 (오타 방지를 위해 변수명 통일)
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
        msg['To'] = target_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(S_EMAIL, S_PASS)
            server.sendmail(S_EMAIL, target_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"메일 발송 실패: {e}")
        return False

# --- 4. 제출 버튼 ---
if st.button("설문 제출하기"):
    if not privacy_agree:
        st.warning("개인정보 동의가 필요합니다.")
    elif name and phone and goals:
        with st.spinner('운영진에게 전송 중...'):
            success = send_email(name, phone, ability, goals, details, ADMIN_LIST[selected_admin])
            if success:
                st.success(f"전송 완료! {selected_admin}님에게 전달되었습니다.")
                st.balloons()
    else:
        st.warning("모든 필수 항목(성함, 연락처, 목적)을 입력해 주세요.")