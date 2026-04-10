import asyncio
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import List
from tools.anomaly_detection import anomaly_detection

load_dotenv()

class RiskAgentOutput(BaseModel):
    risk_summary: str = Field(description="Overall assessment of system risk")
    anomalies_detected: int = Field(description="Total number of anomalies found")
    high_risk_areas: List[str] = Field(description="Metrics or areas with highest risk")
    challenges: List[str] = Field(description="Critical questions or assumptions to verify")
    recommendation: str = Field(description="Suggested next step from risk perspective")


SYSTEM_PROMPT = """
You are a Risk and Critic Agent in a product launch war room.
You MUST use the anomaly_detection tool.
Your responsibilities:
- Identify anomalies in system metrics
- Highlight high-risk areas (e.g., crashes, latency spikes, sudden drops)
- Challenge assumptions made by other teams
- Point out missing data or uncertainties
Guidelines:
- Always call the anomaly_detection tool first
- Base your analysis strictly on detected anomalies
- Be critical and skeptical in your reasoning
- Do NOT make final rollout decisions (no Proceed/Pause/Rollback)
Focus on:
- What could go wrong
- Where the system is unstable
- What needs immediate validation
Output Requirements:
- Return ONLY structured output matching the schema
"""

model = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[anomaly_detection],
    response_format=RiskAgentOutput
)


async def run_risk_agent():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Analyze anomalies in product metrics and identify risks."
        }
    ]

    response = await agent.ainvoke({"messages": messages})
    return response["structured_response"]

if __name__ == "__main__":
    result = asyncio.run(run_risk_agent())
    print(result)