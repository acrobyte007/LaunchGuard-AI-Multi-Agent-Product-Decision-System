import asyncio
import pandas as pd
from transformers import pipeline

sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

async def analyze_single_feedback(text):
    result = sentiment_classifier(text[:512])[0] 
    return text, result['label']

async def semantic_feedback(feedback_input):
    if isinstance(feedback_input, str):
        df = pd.read_excel(feedback_input)
        feedback_list = df['feedback'].dropna().tolist()
    else:
        feedback_list = feedback_input

    tasks = [analyze_single_feedback(text) for text in feedback_list]
    results = await asyncio.gather(*tasks)

    positive = []
    negative = []
    neutral = []
    key_issues_set = set()

    for text, label in results:
        if label.upper() == "POSITIVE":
            positive.append(text)
        elif label.upper() == "NEGATIVE":
            negative.append(text)
            key_issues_set.add(text)
        else:
            neutral.append(text)

    total = len(feedback_list)
    if len(negative) > len(positive):
        overall = "negative"
    elif len(positive) > len(negative):
        overall = "positive"
    else:
        overall = "neutral"

    return {
        "sentiment_summary": {
            "positive": len(positive),
            "negative": len(negative),
            "neutral": len(neutral),
            "total": total,
            "overall_sentiment": overall
        },
        "key_issues": list(key_issues_set)
    }

