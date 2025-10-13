from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import requests
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Envia dados para o webhook do Make.com
        webhook_url = os.environ.get('MAKE_WEBHOOK_URL', '')
        if webhook_url:
            try:
                data = {
                    'message': 'Mentor IA Service está rodando',
                    'timestamp': str(os.times()),
                    'openai_configured': os.environ.get('OPENAI_API_KEY', 'not set') != 'not set'
                }
                response = requests.post(webhook_url, json=data, timeout=10)
                webhook_status = f'Webhook enviado com sucesso: {response.status_code}'
            except Exception as e:
                webhook_status = f'Erro ao enviar webhook: {str(e)}'
        else:
            webhook_status = 'Webhook URL não configurada'
        
        api_key = os.environ.get('OPENAI_API_KEY', 'not set')
        message = f'''<html>
<head><title>Mentor IA Service</title></head>
<body>
<h1>Mentor IA Service</h1>
<p>OpenAI API Key configured: {"Yes" if api_key != "not set" else "No"}</p>
<p>Webhook status: {webhook_status}</p>
</body>
</html>'''
        self.wfile.write(message.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f'Server running on port {port}')
    server.serve_forever()
