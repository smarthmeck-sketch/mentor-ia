from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import requests
from openai import OpenAI

# Cliente OpenAI com a chave do Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para chamar o GPT
def chamar_gpt(mensagem):
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um mentor de estudos para concursos. Sempre dê feedback claro e objetivo."},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro ao chamar GPT: {e}"

# Função para enviar os dados para o Make
def enviar_para_make(dados):
    url_make = os.getenv("MAKE_WEBHOOK_URL")  # configure no Render
    if not url_make:
        return 500, "URL do webhook Make não configurada"
    try:
        resposta = requests.post(url_make, json=dados, timeout=10)
        return resposta.status_code, resposta.text
    except Exception as e:
        return 500, str(e)

# Manipulador HTTP
class ManipuladorMentorIA(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Exemplo fixo de estudo - pode ser dinâmico depois
        materia = "Matemática Financeira"
        topico = "Juros Compostos"
        questoes = 10
        acertos = 7
        erros = 3

        # Chama GPT para gerar observações
        prompt = f"Explique os principais pontos que devo revisar sobre {topico} em {materia}, considerando que acertei {acertos} de {questoes} questões."
        feedback_gpt = chamar_gpt(prompt)

        # Monta JSON esperado pelo Make
        dados = {
            "desempenho": {
                "materia": materia,
                "topico": topico,
                "questoes_resolvidas": questoes,
                "acertos": acertos,
                "erros": erros,
                "data_estudo": "2025-10-13",
                "observacoes": feedback_gpt
            },
            "revisao": {
                "materia": materia,
                "topico": topico,
                "tipo_revisao": "R1",
                "proxima_revisao": "2025-10-14",
                "nivel_prioridade": "Alta",
                "observacao_revisao": "Revisar fórmulas de montante e taxa efetiva"
            }
        }

        # Envia para o Make
        status, resposta = enviar_para_make(dados)

        # Retorna no navegador / Postman
        resposta_final = {
            "status": status,
            "resposta_make": resposta,
            "feedback_gpt": feedback_gpt,
            "dados_enviados": dados
        }
        self.wfile.write(json.dumps(resposta_final, ensure_ascii=False, indent=2).encode("utf-8"))

# Rodar servidor
if __name__ == "__main__":
    porta = int(os.getenv("PORT", 8000))
    servidor = HTTPServer(("0.0.0.0", porta), ManipuladorMentorIA)
    print(f"🚀 Servidor Mentor IA rodando na porta {porta}")
    servidor.serve_forever()
