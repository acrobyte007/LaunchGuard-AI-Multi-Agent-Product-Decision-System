from tools.anomaly_detection import anomaly_detection
import asyncio

file_path = r"data\product_metrics_variable.csv"

print(asyncio.run(anomaly_detection(file_path)))