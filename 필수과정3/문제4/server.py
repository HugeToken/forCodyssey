from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime
import urllib.request
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_location(ip):
    if ip.startswith('127.') or ip == '::1':
        return '로컬 접속'

    try:
        url = f'http://ip-api.com/json/{ip}?lang=ko'
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['status'] == 'success':
                country = data.get('country', '')
                region = data.get('regionName', '')
                city = data.get('city', '')
                return f'{country} {region} {city}'
            else:
                return '위치 정보 조회 실패'
    except Exception as e:
        return f'위치 정보 오류: {e}'

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = get_location(client_ip)
        print(f'접속 시간: {now}, 클라이언트 IP: {client_ip}, 위치: {location}')

        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    server = HTTPServer(('', 8080), MyHandler)
    print('Server running on port 8080... (BASE_DIR={})'.format(BASE_DIR))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('서버가 종료됩니다.')
        server.server_close()
