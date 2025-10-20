# sendmail2.py
import os
import csv
import smtplib
from email.message import EmailMessage

SMTP_HOST = 'smtp.naver.com'
SMTP_PORT = 587

CSV_FILENAME = 'mail_target_list.csv'

def load_recipients(csv_path):
    recipients = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as fh:
            reader = csv.reader(fh)
            for row in reader:
                if not row:
                    continue
                if len(row) < 2:
                    continue
                name = row[0].strip()
                email = row[1].strip()
                if not name or not email:
                    continue
                recipients.append((name, email))
    except Exception as e:
        print('CSV 로드 중 오류:', e)
    return recipients

def make_message(from_addr, to_addr, to_name):
    msg = EmailMessage()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'HTML 테스트 메일'
    plain = f'{to_name}님,\n\n HTML 형식 메일입니다.\n\n감사합니다.'
    html = f"""\
<html>
  <body>
    <p>{to_name}님,</p>
    <p><b>sendmail.py</b> 테스트입니다 — 이 메일은 <i>HTML 형식</i>으로 발송되었습니다.</p>
  </body>
</html>
"""
    msg.set_content(plain)
    msg.add_alternative(html, subtype='html')
    return msg

def main():
    user = os.environ.get('NAVER_USER')
    pwd  = os.environ.get('NAVER_PASS')
    if not (user and pwd):
        print('환경변수 NAVER_USER/NAVER_PASS를 설정한 뒤 실행하세요.')
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, CSV_FILENAME)

    recipients = load_recipients(csv_path)
    if not recipients:
        print('보낼 대상이 없습니다. CSV 파일을 확인하세요:', csv_path)
        return

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(user, pwd)
            for name, addr in recipients:
                msg = make_message(user, addr, name)
                try:
                    smtp.send_message(msg)
                    print('발송 완료:', addr)
                except Exception as e:
                    print('발송 실패:', addr, '->', e)
        print('전체 발송 작업 완료.')
    except Exception as e:
        print('SMTP 연결/전송 실패:', e)
        return

if __name__ == '__main__':
    main()