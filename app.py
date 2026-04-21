import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 페이지 설정
st.set_page_config(page_title="AI 설문조사", layout="centered")

st.title("📋 AI 설문조사")
st.write("본 설문에 참여해 주셔서 감사합니다.")

# 설문 항목
with st.form("survey_form"):
    name = st.text_input("성함")
    phone = st.text_input("연락처")
    answer = st.text_area("AI 모임에 대해 기대하는 점")
    
    submitted = st.form_submit_button("제출하기")

if submitted:
    if not name or not phone:
        st.warning("성함과 연락처를 모두 입력해 주세요.")
    else:
        # Streamlit Secrets에서 설정 정보 가져오기
        try:
            SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
            APP_PASSWORD = st.secrets["APP_PASSWORD"]
            RECEIVER_EMAIL = st.secrets["RECEIVER_EMAIL"]

            # 이메일 내용 구성 (한글 지원을 위해 MIMEText 사용)
            subject = f"[설문응답] {name}님의 응답입니다."
            body = f"성함: {name}\n연락처: {phone}\n응답내용: {answer}"
            
            # 한글 인코딩 설정
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL

            # 메일 보내기
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            
            st.success("✅ 성공적으로 제출되었습니다. 감사합니다!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ 발송 실패: {e}")
            st.info("Secrets 설정을 다시 확인해 주세요.")