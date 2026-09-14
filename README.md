<p align="center">
  <img src="https://img.shields.io/github/license/f3mattos/telemetry-ai-agent?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/f3mattos/telemetry-ai-agent?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/issues/f3mattos/telemetry-ai-agent?style=for-the-badge" alt="Issues">
  <img src="https://img.shields.io/badge/python-v3.10+-blue?style=for-the-badge&logo=python" alt="Python Version">
</p>

<h1 align="center"> Telemetria industrial com Agentes de IA</h1>

<p align="center">
  <b>Sistema Híbrido IIoT: Detecção de Anomalias via Deep Learning na Borda e Diagnóstico Executivo com IA Generativa na Nuvem.</b>
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-tecnologias">Tecnologias</a> •
  <a href="#-como-executar">Como Executar</a> •
  <a href="#-api-endpoints">API Endpoints</a> •
  <a href="#-autor">Autor</a> •
  <a href="#-licença">Licença</a>
</p>

---

## 📌 Sobre o Projeto

O **Telemetria industrial com Agentes de IA** resolve o desafio de monitorar sensores de alta frequência em ambientes industriais sem inflar os custos com chamadas recorrentes a LLMs.

A solução adota uma **arquitetura em duas camadas**:
1. **Edge:** Um Autoencoder em PyTorch processa 100% da telemetria contínua (temperatura, vibração e pressão), identificando desvios numéricos com baixíssima latência.
2. **Cloud:** Apenas os eventos que violam o limiar crítico (MSE) são encaminhados para a **Responses API da OpenAI**, gerando laudos em linguagem executiva focados em causa raiz e tomada de decisão para a alta gestão.

---

## ✨ Funcionalidades

- [x] **Processamento na Borda:** Detecção contínua de anomalias com Autoencoders (Deep Learning).
- [x] **Filtragem Inteligente:** Redução de custos e volume de dados ao disparar a IA Generativa somente em inconsistências térmicas, mecânicas ou hidráulicas.
- [x] **Laudos Executivos C-Level:** Tradução automática de desvios técnicos em pareceres operacionais diretos sem jargões de IA.
- [x] **API REST Integrada:** Endpoints assíncronos via FastAPI para consumo por dashboards e sistemas SCADA.
- [x] **Gestão de Segurança:** Isolamento de credenciais com variáveis de ambiente (`.env`).

---




##  Arquitetura

```mermaid
graph TD
    A[Sensoriamento Industrial] -->|Telemetria Contínua| B(Edge: PyTorch Autoencoder)
    B -->|"Operação Nominal (MSE < Limiar)"| C[Dados Descartados / Operação Normal]
    B -->|"Anomalia (MSE > Limiar)"| D(Cloud: OpenAI Responses API)
    D -->|Relatório Gerencial Executivo| E[Dashboard / Alertas C-Level]
 Tecnologias
As seguintes ferramentas foram utilizadas na construção do projeto:

Python 3.10+

PyTorch — Treinamento e inferência da rede neural Autoencoder

OpenAI API — Geração de texto gerencial via Responses API

FastAPI & Uvicorn — Construção da interface REST

Pandas & Scikit-Learn — Normalização e tratamento de matrizes numéricas

Python-Dotenv — Carregamento de variáveis de ambiente

 Como Executar
Pré-requisitos
Antes de começar, você precisará ter instalado em sua máquina:

Git

Python 3.10 ou superior

📊 Passo a Passo
Bash
# 1. Clone este repositório
$ git clone [https://github.com/f3mattos/telemetry-ai-agent.git](https://github.com/f3mattos/telemetry-ai-agent.git)

# 2. Acesse a pasta do projeto
$ cd telemetry-ai-agent

# 3. Crie e ative o ambiente virtual
$ python -m venv .venv

# No Windows (PowerShell):
$ .\.venv\Scripts\activate
# No Linux/Mac:
$ source .venv/bin/activate

# 4. Instale as dependências
$ pip install -r requirements.txt
🔑 Configuração das Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto (no mesmo nível da pasta src/):

Snippet de código
OPENAI_API_KEY=sk-proj-sua_chave_aqui
⚙️ Executando a Aplicação
Modo CLI (Pipeline Local):

Bash
python -m src.main
Modo API REST (Servidor Web):

Bash
uvicorn src.api:app --reload
Acesse a documentação Swagger interativa em: http://127.0.0.1:8000/docs

 API Endpoints
POST /api/v1/analyze
Processa um lote de telemetria e retorna o diagnóstico do Autoencoder com o laudo executivo da OpenAI (se houver anomalia).

Exemplo de Payload:

JSON
{
  "equipamento": "BOMBA_IND_01",
  "readings": [
    {"temp": 64.8, "vibr": 1.49, "press": 4.02},
    {"temp": 101.5, "vibr": 4.75, "press": 1.72},
    {"temp": 64.9, "vibr": 1.50, "press": 4.01}
  ]
}
Exemplo de Resposta:

JSON
{
  "borda_diagnostico": {
    "equipamento": "BOMBA_IND_01",
    "total_leituras": 3,
    "anomalias_detectadas": 1,
    "limiar_tolerado_mse": 0.0842,
    "pior_erro_registrado": 2.4158,
    "eventos_criticos": [
      {"temp": 101.5, "vibr": 4.75, "press": 1.72}
    ]
  },
  "laudo_c_level": "RELATÓRIO DE RISCO OPERACIONAL...\n\nEquipamento: BOMBA_IND_01\nStatus: Alerta Crítico de Temperatura e Vibração...\nRecomendação: Interrupção imediata para inspeção do selo mecânico e rolamentos."
}
 Contribuição
Contribuições são sempre bem-vindas! Para contribuir:

Faça um Fork do projeto.

Crie uma Branch para sua Feature (git checkout -b feature/NovaFeature).

Faça o Commit das suas alterações (git commit -m 'feat: Adiciona nova feature').

Faça o Push para a Branch (git push origin feature/NovaFeature).

Abra um Pull Request.

📝 Licença
Este projeto está sob a licença MIT.

👤 Autor
Feito por Felipe Mattos!