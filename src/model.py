import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class IndustrialAutoencoder(nn.Module):
    def __init__(self, input_dim=3):
        super(IndustrialAutoencoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, 2), nn.ReLU())
        self.decoder = nn.Sequential(nn.Linear(2, input_dim))

    def forward(self, x):
        return self.decoder(self.encoder(x))

class TelemetryDetector:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IndustrialAutoencoder(input_dim=3)
        self.limiar_mse = 0.0

    def fit_baseline(self, df_nom: pd.DataFrame):
        X_train = self.scaler.fit_transform(df_nom)
        X_tensor = torch.FloatTensor(X_train)
        
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)

        for _ in range(80):
            optimizer.zero_grad()
            outputs = self.model(X_tensor)
            loss = criterion(outputs, X_tensor)
            loss.backward()
            optimizer.step()

        with torch.no_grad():
            rec = self.model(X_tensor)
            erros = torch.mean((X_tensor - rec) ** 2, dim=1).numpy()
            self.limiar_mse = float(np.percentile(erros, 98))

    def analyze(self, df_teste: pd.DataFrame) -> dict:
        X_test = self.scaler.transform(df_teste[["temp", "vibr", "press"]])
        X_tensor = torch.FloatTensor(X_test)
        
        with torch.no_grad():
            rec = self.model(X_tensor)
            erros = torch.mean((X_tensor - rec) ** 2, dim=1).numpy()

        df_teste["is_anomaly"] = erros > self.limiar_mse
        anomalias = df_teste[df_teste["is_anomaly"]]

        return {
            "equipamento": "BOMBA_IND_01",
            "total_leituras": len(df_teste),
            "anomalias_detectadas": len(anomalias),
            "limiar_tolerado_mse": round(self.limiar_mse, 4),
            "pior_erro_registrado": round(float(erros.max()), 4),
            "eventos_criticos": anomalias[["temp", "vibr", "press"]].to_dict(orient="records")
        }