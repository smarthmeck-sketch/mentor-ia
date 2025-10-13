from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        api_key = os.environ.get('OPENAI_API_KEY', 'not set')
        message = f'<h1>Mentor IA Service</h1><p>OpenAI API Key configured: {"Yes" if api_key != "not set" else "No"}</p>'
        self.wfile.write(message.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f'Server running on port {port}')
    server.serve_forever()
