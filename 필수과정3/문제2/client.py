import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None

    def start_client(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print('서버에 연결할 수 없습니다:', e)
            sys.exit()

        server_msg = self.client_socket.recv(1024).decode('utf-8')
        sys.stdout.write(server_msg)
        sys.stdout.flush()
        self.nickname = input().strip()
        self.client_socket.send(self.nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    print('서버와 연결이 끊어졌습니다.')
                    break

                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write(message + '\n')
                sys.stdout.flush()

                sys.stdout.write(f'[{self.nickname}]: ')
                sys.stdout.flush()
            except:
                break

    def send_messages(self):
        try:
            while True:
                sys.stdout.write(f'[{self.nickname}]: ')
                sys.stdout.flush()
                message = input()

                if message.strip() == '/종료':
                    self.client_socket.send(message.encode('utf-8'))
                    break
                self.client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            self.client_socket.send('/종료'.encode('utf-8'))
        finally:
            self.client_socket.close()
            print('\n연결을 종료합니다.')

if __name__ == '__main__':
    client = ChatClient()
    client.start_client()
