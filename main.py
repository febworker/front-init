from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import socket
import json
from datetime import datetime
import os

PORT_HTTP = 3000
PORT_SOCKET = 5000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/message':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('style.css', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/logo.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo.png', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            form_data = {}
            for item in post_data.split('&'):
                key, value = item.split('=')
                form_data[key] = value

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())

            # Виклик функції save_data_to_json для збереження даних у файл
            self.save_data_to_json(form_data)
        else:
            self.send_error(404, "Page not found")

    # Функція для збереження даних у JSON файл і обробки помилок
    def save_data_to_json(self, data):
        try:
            os.makedirs('storage', exist_ok=True)
            with open('storage/data.json', 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}
        except ValueError as ve:
            print(f"Error parsing JSON: {ve}")
            return

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        json_data[current_time] = data

        with open('storage/data.json', 'w') as file:
            json.dump(json_data, file, indent=4)

class SocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, _ = self.request
        received_data = json.loads(data.decode('utf-8'))
        HttpHandler().save_data_to_json(received_data)

def run_http_server():
    with HTTPServer(('0.0.0.0', PORT_HTTP), HttpHandler) as http_server:
        print(f"HTTP server running on port {PORT_HTTP}")
        http_server.serve_forever()

def run_socket_server():
    with socketserver.UDPServer(('0.0.0.0', PORT_SOCKET), SocketHandler) as sock_server:
        print(f"Socket server running on port {PORT_SOCKET}")
        sock_server.serve_forever()

if __name__ == "__main__":
    import threading

    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()

    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()