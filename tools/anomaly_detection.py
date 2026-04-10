import asyncio
import pandas as pd
import numpy as np
from langchain.tools import tool

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

path=r"data\product_metrics_variable.csv"

@tool
async def anomaly_detection():
    """
    Detect anomalies in time-series metrics using statistical deviation (Z-score).

    This tool analyzes numeric metrics from a preloaded dataset and identifies
    data points that significantly deviate from the mean.

    Returns:
        dict:
            {
                "anomalies": [
                    {
                        "metric": str,
                        "index": int,
                        "value": float,
                        "z_score": float
                    }
                ],
                "total_anomalies": int
            }

    Notes:
        - Operates on internally defined dataset
        - Automatically detects numeric columns
        - Uses Z-score threshold (|z| > 2) for anomaly detection
        - Designed for Data Analyst and Risk agents
    """
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