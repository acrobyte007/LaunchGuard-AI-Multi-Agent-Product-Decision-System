import asyncio
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import List
from tools.feedback_scoring import semantic_feedback_tool

load_dotenv()


class MarketingAgentOutput(BaseModel):
    sentiment_summary: str = Field(description="Overall sentiment insight")
    key_issues: List[str] = Field(description="Main user complaints")
    positive_signals: List[str] = Field(description="Positive feedback highlights")
    communication_risk: str = Field(description="Low / Medium / High")
    recommendation: str = Field(description="Communication action plan")


SYSTEM_PROMPT = """
You are a Marketing and Communications Agent in a product launch war room.
You MUST use the semantic_feedback_tool.
Responsibilities:
- Understand overall sentiment
- Identify key issues from negative feedback
- Highlight positive signals
- Assess communication risk
Rules:
- Always call the tool first
- Base answer strictly on tool output
- Do NOT make product decisions
Return ONLY structured output.
"""


model = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[semantic_feedback_tool],
    response_format=MarketingAgentOutput
)


async def run_marketing_agent():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Analyze user feedback and provide sentiment insights."
        }
    ]

    response = await agent.ainvoke({"messages": messages})
    return response["structured_response"]


if __name__ == "__main__":
    result = asyncio.run(run_marketing_agent())
    print(result)