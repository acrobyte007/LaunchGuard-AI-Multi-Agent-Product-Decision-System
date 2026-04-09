from tools.metrics import summarize_metrics
import asyncio

csv_file_path = r"data\product_metrics_variable.csv"
print(asyncio.run(summarize_metrics(csv_file_path)))