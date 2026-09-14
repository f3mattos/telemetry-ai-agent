import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Define a raiz do projeto (subindo um nível a partir de src/)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Carrega explicitamente o arquivo na raiz
load_dotenv(dotenv_path=ENV_FILE)

class ExecutiveAgent:
    def __init__(self, model_name: str = "gpt-5.6-luna"):
        # Tenta pegar do .env ou das variáveis de ambiente do sistema
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                f"OPENAI_API_KEY não foi encontrada.\n"
                f"Caminho procurado: {ENV_FILE}\n"
                f"Verifique se o arquivo existe nesse local exato e se a linha está como OPENAI_API_KEY=sua_chave"
            )
        
        self.client = OpenAI(api_key=api_key, timeout=60.0, max_retries=3)
        self.model_name = model_name

    def generate_report(self, anomaly_data: dict) -> str:
        if anomaly_data["anomalias_detectadas"] == 0:
            return "Operação nominal sem desvios."

        instrucao = (
            "Você é o Diretor de Operações de Planta Industrial. "
            "Traduza métricas de falhas de Autoencoders em um relatório direto para o C-Level. "
            "Foque em: Risco de Parada de Linha, Causa Raiz Provável, Impacto Financeiro "
            "e Decisão Corretiva Imediata. Não use jargões de inteligência artificial."
        )

        prompt = (
            f"Alerta de Anomalia Crítica no Equipamento: {anomaly_data['equipamento']}\n"
            f"- Leituras no Lote: {anomaly_data['total_leituras']}\n"
            f"- Pontos com Falha: {anomaly_data['anomalias_detectadas']}\n"
            f"- Pior Desvio Registrado (MSE): {anomaly_data['pior_erro_registrado']} (Limite Seguro: {anomaly_data['limiar_tolerado_mse']})\n"
            f"- Dados de Telemetria da Falha: {anomaly_data['eventos_criticos']}\n"
        )

        response = self.client.responses.create(
            model=self.model_name,
            instructions=instrucao,
            input=prompt,
            reasoning={"effort": "low"},
            text={"verbosity": "medium"}
        )

        print(f"\n[CONSUMO] Tokens Saída: {response.usage.output_tokens} | Total: {response.usage.total_tokens}")
        return response.output_text