import asyncio
import pandas as pd
import numpy as np

async def detect_column(df, col):
    s = df[col].dropna()
    m = s.mean()
    sd = s.std()
    if sd == 0:
        return []
    z = (s - m) / sd
    return [
        {
            "metric": col,
            "index": int(i),
            "value": float(s.iloc[i]),
            "z_score": float(round(z.iloc[i], 2))
        }
        for i in range(len(z)) if abs(z.iloc[i]) > 2
    ]

async def anomaly_detection(path):
    try:
        df = pd.read_csv(path)
    except:
        df = pd.read_excel(path)
    cols = df.select_dtypes(include=[np.number]).columns
    tasks = [detect_column(df, c) for c in cols]
    res = await asyncio.gather(*tasks)
    anomalies = [x for sub in res for x in sub]
    return {
        "anomalies": anomalies,
        "total_anomalies": len(anomalies)
    }