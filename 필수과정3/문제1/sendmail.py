# sendmail.py
import os
import smtplib
from email.message import EmailMessage

def main():
    MY_EMAIL = os.environ.get('GMAIL_USER')
    MY_PASS  = os.environ.get('GMAIL_PASS')
    TO_EMAIL = os.environ.get('GMAIL_TO', MY_EMAIL)

    if not (MY_EMAIL and MY_PASS):
        print('환경변수 GMAIL_USER / GMAIL_PASS 를 설정한 뒤 실행하세요.')
        return

    script_file = os.path.abspath(__file__) 
    script_folder = os.path.dirname(script_file)
    attach_path = os.path.join(script_folder, 'test.png')

    if not os.path.exists(attach_path):
        print('첨부 파일 없음:', attach_path)
        return

    msg = EmailMessage()
    msg['From'] = MY_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = 'sendmail.py 테스트 메일'
    msg.set_content('test.png 파일 첨부 테스트 메일 전송 확인.')

    with open(attach_path, 'rb') as f:
        data = f.read()
    msg.add_attachment(data, maintype='image', subtype='png', filename=os.path.basename(attach_path))

    SMTP_HOST = 'smtp.gmail.com'
    try:
        with smtplib.SMTP(SMTP_HOST, 587, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(MY_EMAIL, MY_PASS)
            smtp.send_message(msg)
        print('메일 전송 성공')
    except Exception as e:
        print('전송 실패:', e)
        return

if __name__ == '__main__':
    main()