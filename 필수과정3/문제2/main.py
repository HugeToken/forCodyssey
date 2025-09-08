import socket
import threading
import sys

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()
        self.running = True

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.settimeout(1.0)

        print('채팅 서버가 시작되었습니다. (Ctrl+C 로 종료)')

        try:
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(conn,)).start()
                    threading.daemon = True
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print('\n서버를 종료합니다...')
            self.shutdown_server()
            sys.exit()

    def broadcast(self, message, exclude=None):
        with self.lock:
            for client in list(self.clients.keys()):
                if client != exclude:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        client.close()
                        self.remove_client(client)

    def send_to_nickname(self, sender_conn, target_nickname, message):
        sender_name = self.clients.get(sender_conn, '알수없음')
        with self.lock:
            target_conn = None
            for conn, name in self.clients.items():
                if name == target_nickname:
                    target_conn = conn
                    break

            if target_conn:
                try:
                    print(f'[귓속말] {sender_name} -> {target_nickname} : {message}')

                    whisper_msg = f'[{sender_name}] 님에게 온 귓속말 : {message}'
                    target_conn.send(whisper_msg.encode('utf-8'))

                    sender_conn.send(f'[{target_nickname}] 님에게 귓속말 보냄 : {message}'.encode('utf-8'))
                except:
                    pass
            else:
                sender_conn.send(f'[{target_nickname}] 닉네임은 존재하지 않습니다.'.encode('utf-8'))

    def handle_client(self, conn):
        try:
            conn.send('닉네임을 입력하세요: '.encode('utf-8'))
            nickname = conn.recv(1024).decode('utf-8').strip()
            with self.lock:
                self.clients[conn] = nickname

            welcome_message = f'[{nickname}] 님이 입장하셨습니다.'
            print(welcome_message)
            self.broadcast(welcome_message)

            while True:
                message = conn.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                if message == '/종료':
                    exit_message = f'[{nickname}] 님이 퇴장하셨습니다.'
                    print(exit_message)
                    self.broadcast(exit_message, exclude=conn)
                    break
                elif message.startswith('/w '):
                    parts = message.split(' ', 2)
                    if len(parts) < 3:
                        conn.send('사용법: /w 닉네임 메시지'.encode('utf-8'))
                    else:
                        target_nickname = parts[1]
                        whisper_content = parts[2]
                        self.send_to_nickname(conn, target_nickname, whisper_content)
                else:
                    formatted_message = f'[{nickname}] : {message}'
                    print(formatted_message)
                    self.broadcast(formatted_message, exclude=conn)
        except:
            pass
        finally:
            self.remove_client(conn)

    def remove_client(self, conn):
        with self.lock:
            if conn in self.clients:
                del self.clients[conn]
        conn.close()

    def shutdown_server(self):
        self.running = False
        with self.lock:
            for conn in list(self.clients.keys()):
                try:
                    conn.close()
                except:
                    pass
            self.clients.clear()
        self.server_socket.close()

if __name__ == '__main__':
    server = ChatServer()
    server.start_server()
