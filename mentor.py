from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests
import json

class ManipuladorSimples(BaseHTTPRequestHandler):
    def do_GET(self):
        # Envia resposta HTTP básica
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # URL do webhook Make.com
        WEBHOOK_URL = "https://hook.us2.make.com/axp36f1x67bdwmvje2h8kfyqgkxea2co"

        # Payload solicitado (desempenho e revisão)
        payload = {
            "desempenho": {
                "materia": "Matemática Financeira",
                "topico": "Juros Compostos",
                "questoes_resolvidas": 10,
                "acertos": 7,
                "erros": 3,
                "nivel_dificuldade": "Médio",
                "nivel_desempenho": "Regular",
                "data_estudo": "2025-10-12",
                "observacoes": "Confundi taxa efetiva com nominal.",
                "progresso": "70%",
                "tendencia": "Melhorando"
            },
            "revisao": {
                "materia": "Matemática Financeira",
                "topico": "Juros Compostos",
                "tipo_revisao": "R1",
                "status_revisao": "Agendada",
                "proxima_revisao": "2025-10-13",
                "nivel_prioridade": "Alta",
                "observacao_revisao": "Revisar fórmulas de montante e taxa efetiva."
            }
        }

        # Envia para o webhook
        status_do_webhook = "Não enviado"
        try:
            headers = {"Content-Type": "application/json"}
            resposta = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload), timeout=10)
            status_do_webhook = f"Webhook enviado com sucesso: {resposta.status_code}"
        except Exception as e:
            status_do_webhook = f"Erro ao enviar webhook: {str(e)}"

        # HTML de resposta
        chave_api = os.getenv("ABRIR_CHAVE_API", "não definido")
        html = f"""
        <h1>Serviço Mentor IA</h1>
        <p>Chave de API OpenAI configurada: {'Sim' if chave_api != 'não definido' else 'Não'}</p>
        <p>Status do webhook: {status_do_webhook}</p>
        """
        self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    porta = int(os.getenv('PORT', '8000'))
    servidor = HTTPServer(('', porta), ManipuladorSimples)
    print(f"Servidor rodando na porta {porta}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    servidor.server_close()
