from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests
import json

class ManipuladorSimples(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Envia dados para o webhook do Make
        URL_do_webhook = os.getenv('CRIAR_URL_WEBHOOK', '')
        if URL_do_webhook:
            try:
                dados = {
                    "mensagem": "Mentor IA Service está rodando",
                    "carimbo_data": str(os.times()),
                    "openai_configurado": os.getenv("ABRIR_CHAVE_API", "não definido")
                }
                resposta = requests.post(URL_do_webhook, json=dados, timeout=10)
                status_do_webhook = f"Webhook enviado com sucesso: {resposta.status_code}"
            except Exception as e:
                status_do_webhook = f"Erro ao enviar webhook: {str(e)}"
        else:
            status_do_webhook = "URL do webhook não definido"

        chave_api = os.getenv("ABRIR_CHAVE_API", "não definido")
        mensagem = f"""
        <html>
        <head><title>Serviço Mentor IA</title></head>
        <body>
        <h1>Serviço Mentor IA</h1>
        <p>Chave de API OpenAI configurada: {"Sim" if chave_api != "não definido" else "Não"}</p>
        <p>Status do webhook: {status_do_webhook}</p>
        </body>
        </html>
        """
        self.wfile.write(mensagem.encode())

if __name__ == "__main__":
    porta = int(os.getenv("PORTA", 8000))
    servidor = HTTPServer(("0.0.0.0", porta), ManipuladorSimples)
    print(f"Servidor em execução na porta {porta}")
    servidor.serve_forever()
