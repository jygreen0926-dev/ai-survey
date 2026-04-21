import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# --- 1. 운영진 정보 설정 ---
ADMIN_LIST = {
    "유미짱": "Yoomic663@gmail.com", 
    "제제": "jygreen0926@gmail.com"
}

# 페이지 설정
st.set_page_config(page_title="AI 모임리서치", layout="centered")

# URL 파라미터로 운영진 자동 선택
query_params = st.query_params
default_admin = query_params.get("admin", "유미짱")

# --- 2. UI 부분 ---
st.title("🚀 AI 모임 리서치 앱")

# 개인정보 유의사항 문구 추가
st.info("""
**[개인정보 수집 및 이용 안내]**
* 수집 항목: 성함, 연락처, AI 역량, 참여 목적 등
* 수집 목적: AI 모임 운영 및 안내 연락
* 보유 기간: 목적 달성 후 즉시 파기
""")

# 담당 운영진 선택
selected_admin = st.selectbox(
    "담당 운영진", 
    options=list(ADMIN_LIST.keys()),
    index=list(ADMIN_LIST.keys()).index(default_admin) if default_admin in ADMIN_LIST else 0
)

# 설문 항목들 (연락처 칸 복구!)
name = st.text_input("성함")
phone = st.text_input("연락처 (예: 010-0000-0000)") # 연락처 칸 추가
ability = st.radio("AI 역량", ["입문자", "초보자", "숙련자", "전문가"])
goals = st.multiselect("참여 목적", ["유튜브", "친목", "자기계발", "사업 활용"])
details = st.text_area("상세 목표")

# 개인정보 동의 체크박스 (보통 유의사항과 세트죠!)
privacy_agree = st.checkbox("개인정보 수집 및 이용에 동의합니다.")

def send_email(name, phone, ability, goals, details, target_email):
    try:
        S_EMAIL = st.secrets["SENDER_EMAIL"]
        S_PASS = st.secrets["APP_PASSWORD"]
        
        subject = f"[AI 모임] {name}님의 참여 신청서 (담당: {selected_admin})"
        body = f"""
        새로운 설문 응답이 도착했습니다!
        
        [담당 운영진: {selected_admin}]
        1. 성함: {name}
        2. 연락처: {phone}
        3. 역량: {ability}
        4. 목적: {", ".join(goals)}
        5. 상세내용: {details}
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
    if not privacy_agree:
        st.warning("개인정보 수집 및 이용에 동의해 주세요.")
    elif name and phone and goals:
        with st.spinner(f'{selected_admin}님에게 전송 중...'):
            target_addr = ADMIN_LIST[selected_admin]
            success = send_email(name, phone, ability, goals, details, target_addr)
            if success:
                st.success(f"감사합니다, {name}님! {selected_admin}님에게 응답이 전달되었습니다.")
                st.balloons()
    else:
        st.warning("모든 필수 항목(성함, 연락처, 목적)을 입력해 주세요.")