import asyncio
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import List, Dict, Any
load_dotenv()

class PMAgentOutput(BaseModel):
    decision: str = Field(description="Proceed / Pause / Roll Back")
    rationale: str = Field(description="Key reasons with metrics and feedback references")
    risk_register: List[Dict[str, str]] = Field(description="Top risks with mitigation")
    action_plan: List[Dict[str, str]] = Field(description="Actions for next 24-48 hours with owners")
    communication_plan: str = Field(description="Internal and external communication guidance")
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    confidence_improvement: str = Field(description="What additional data would improve confidence")

SYSTEM_PROMPT = """
You are the Product Manager (PM) Agent in a product launch war room.
Your role:
- Make the FINAL decision: Proceed / Pause / Roll Back
- Combine inputs from:
  1. Data Analyst (metrics trends)
  2. Marketing Agent (user sentiment)
  3. Risk Agent (anomalies and risks)
  4. Release Notes (feature context, known issues, success criteria)
Decision Guidelines:
Proceed:
- Metrics stable or improving
- Low crash rate and latency
- Positive or neutral sentiment
- No major risks
Pause:
- Some metrics degrading
- Moderate risks or anomalies
- Mixed or negative sentiment
- Needs investigation
Roll Back:
- Critical failures (high crash rate, severe latency)
- Strong negative sentiment
- Multiple high-risk anomalies
- Violates success criteria
Instructions:
- Use metric references explicitly (e.g., crash rate increasing, latency > threshold)
- Cross-check with release note success criteria
- Consider known issues and whether they are occurring
- Be decisive and realistic
Output Rules:
- Return ONLY structured output
- Do NOT include explanation outside schema
- Be concise but informative
Focus:
- User impact
- System stability
- Business risk
"""
model = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[],
    response_format=PMAgentOutput
)

async def run_pm_agent(
    data_analyst_output: dict,
    marketing_output: dict,
    risk_output: dict,
    release_notes: str
):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Data Analyst Output:
{data_analyst_output}
Marketing Agent Output:
{marketing_output}
Risk Agent Output:
{risk_output}
Release Notes:
{release_notes}
Make the final launch decision.
"""
        }
    ]
    response = await agent.ainvoke({"messages": messages})
    return response["structured_response"]

