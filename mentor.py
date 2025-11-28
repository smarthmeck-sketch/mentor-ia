from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

# Manipulador HTTP
class ManipuladorMentorIA(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Dados de exemplo de desempenho de estudo
        resposta_final = {
            "status": "ok",
            "servico": "Mentor IA - Bancários",
            "desempenho": {
                "materia": "Matemática Financeira",
                "topico": "Juros Compostos",
                "questoes_resolvidas": 10,
                "acertos": 7,
                "erros": 3,
                "data_estudo": "2025-11-28",
                "observacoes": "Bom desempenho. Revise as fórmulas de taxa efetiva."
            },
            "revisao": {
                "materia": "Matemática Financeira",
                "topico": "Juros Compostos",
                "tipo_revisao": "R1",
                "proxima_revisao": "2025-11-29",
                "nivel_prioridade": "Alta",
                "observacao_revisao": "Revisar fórmulas de montante e taxa efetiva"
            }
        }
        
        self.wfile.write(json.dumps(resposta_final, ensure_ascii=False, indent=2).encode("utf-8"))
    
    def log_message(self, format, *args):
        # Suprimir logs padrão do servidor
        pass

# Rodar servidor
if __name__ == "__main__":
    porta = int(os.getenv("PORT", 8000))
    servidor = HTTPServer(("0.0.0.0", porta), ManipuladorMentorIA)
    print(f"🚀 Servidor Mentor IA rodando na porta {porta}")
    servidor.serve_forever()
