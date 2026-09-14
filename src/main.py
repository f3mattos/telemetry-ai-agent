import numpy as np
import pandas as pd
from model import TelemetryDetector
from agent import ExecutiveAgent

def run_pipeline():
    # 1. Gera baseline e treina Autoencoder
    np.random.seed(42)
    df_treino = pd.DataFrame({
        "temp": np.random.normal(65.0, 2.0, 1000),
        "vibr": np.random.normal(1.5, 0.15, 1000),
        "press": np.random.normal(4.0, 0.1, 1000)
    })

    detector = TelemetryDetector()
    detector.fit_baseline(df_treino)

    # 2. Simula dados do sensor com uma falha crítica
    lote_teste = pd.DataFrame([
        {"temp": 64.8, "vibr": 1.49, "press": 4.02},
        {"temp": 101.5, "vibr": 4.75, "press": 1.72}, # Falha
        {"temp": 64.9, "vibr": 1.50, "press": 4.01}
    ])

    # 3. Executa a análise na borda
    diagnostico = detector.analyze(lote_teste)
    print(f"Status Borda: {diagnostico['anomalias_detectadas']} anomalia(s) detectada(s).")

    # 4. Gera o laudo executivo
    if diagnostico["anomalias_detectadas"] > 0:
        agent = ExecutiveAgent()
        laudo = agent.generate_report(diagnostico)
        print("\n--- LAUDO GERENCIAL / EXECUTIVO ---")
        print(laudo)

if __name__ == "__main__":
    run_pipeline()