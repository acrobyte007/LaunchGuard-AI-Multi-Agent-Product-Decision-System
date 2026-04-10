import asyncio
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import List
from tools.metrics import summarize_metrics
from tools.anomaly_detection import anomaly_detection

load_dotenv()

class DataAnalystOutput(BaseModel):
    summary: str = Field(description="Short explanation of overall metric trends")
    key_insights: List[str] = Field(description="Important observations from metrics")
    critical_metrics: List[str] = Field(description="Metrics that indicate serious issues")
    recommendation: str = Field(description="Suggested next step based on data")

SYSTEM_PROMPT = """
You are a Data Analyst Agent in a product launch war room.
Your role is to analyze product performance using quantitative data and detect risks.
You MUST use the provided tools:
1. summarize_metrics → to understand trends across all metrics
2. anomaly_detection → to identify abnormal spikes or drops
Your responsibilities:
- Analyze metric trends (increasing, decreasing, stable)
- Identify key insights from the data
- Detect critical issues such as:
  - Rising crash rate
  - Increasing latency
  - Drop in conversion or DAU
  - Spike in support tickets
- Use anomaly detection results to strengthen your findings
Guidelines:
- Always call BOTH tools before forming your answer
- Base your response strictly on tool outputs
- Be concise and data-driven
- Do NOT make final rollout decisions (no Proceed/Pause/Rollback)
Output Requirements:
- Return ONLY structured output matching the given schema
- Do NOT include explanations outside the schema
- Do NOT hallucinate metrics — only use tool results
Focus on:
- What is going wrong
- What is improving
- What needs attention immediately
"""

model = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0
)

agent = create_agent(
    model,
    tools=[summarize_metrics, anomaly_detection],
    response_format=DataAnalystOutput
)


async def run_data_analyst_agent():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Please analyze the product metrics and provide a concise summary."
        }
    ]

    response = await agent.ainvoke({"messages": messages})
    result=(response["structured_response"])
    return result

