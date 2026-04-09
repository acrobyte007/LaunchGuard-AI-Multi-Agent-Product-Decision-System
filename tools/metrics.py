import pandas as pd

async def summarize_metrics(csv_file_path):
    df = pd.read_csv(csv_file_path)
    metrics = [col for col in df.columns if col.lower() != "date"]
    metric_trends = {}
    
    for metric in metrics:
        start_value = df[metric].iloc[0].item()
        end_value = df[metric].iloc[-1].item()
        change = end_value - start_value
        
        if change > 0:
            trend = "increasing"
        elif change < 0:
            trend = "decreasing"
        else:
            trend = "stable"
            
        metric_trends[metric] = {
            "trend": trend,
            "change": round(change, 2),
            "start_value": round(start_value, 2),
            "end_value": round(end_value, 2)
        }
        
    positive_trends = []
    negative_trends = []
    critical_trends = []
    critical_metrics = ["crash_rate_pct", "api_p95_latency_ms", "support_tickets"]
    
    for metric, info in metric_trends.items():
        if metric in critical_metrics and info["trend"] == "increasing":
            critical_trends.append(metric)
        elif info["trend"] == "increasing":
            positive_trends.append(metric)
        elif info["trend"] == "decreasing":
            negative_trends.append(metric)
            
    summary = {
        "positive_trends": positive_trends,
        "negative_trends": negative_trends,
        "critical_trends": critical_trends
    }
    
    return {
        "metric_trends": metric_trends,
        "summary": summary
    }
