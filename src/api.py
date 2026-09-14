from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from src.model import TelemetryDetector
from src.agent import ExecutiveAgent

app = FastAPI(title="Industrial Telemetry AI Agent", version="1.0")

# Inicializa e treina baseline localmente na inicialização
detector = TelemetryDetector()
df_treino = pd.DataFrame({
    "temp": np.random.normal(65.0, 2.0, 1000),
    "vibr": np.random.normal(1.5, 0.15, 1000),
    "press": np.random.normal(4.0, 0.1, 1000)
})
detector.fit_baseline(df_treino)

class TelemetryItem(BaseModel):
    temp: float
    vibr: float
    press: float

class TelemetryBatch(BaseModel):
    equipamento: str
    readings: list[TelemetryItem]

@app.post("/api/v1/analyze")
def analyze_telemetry(payload: TelemetryBatch):
    try:
        data = [item.dict() for item in payload.readings]
        df_teste = pd.DataFrame(data)
        
        # 1. Executa Autoencoder na borda
        diagnostico = detector.analyze(df_teste)
        diagnostico["equipamento"] = payload.equipamento
        
        # 2. Executa LLM apenas se houver anomalias
        laudo_executivo = "Operação nominal sem desvios."
        if diagnostico["anomalias_detectadas"] > 0:
            agent = ExecutiveAgent()
            laudo_executivo = agent.generate_report(diagnostico)
            
        return {
            "borda_diagnostico": diagnostico,
            "laudo_c_level": laudo_executivo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))