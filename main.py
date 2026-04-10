import asyncio
import logging
from dotenv import load_dotenv
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from agents.data_analyst_agent import run_data_analyst_agent
from agents.marketing_agent import run_marketing_agent
from agents.risk_agent import run_risk_agent
from agents.product_manager_agent import run_pm_agent

load_dotenv()

logging.basicConfig(
    filename="war_room.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

RELEASE_NOTES = """
Feature: Smart Auto-Pay for Subscriptions
Overview:
Auto payment for subscriptions.
Success Metrics:
- Crash rate < 2%
- Latency < 400 ms
- Adoption > 60%
Known Issues:
- Payment failures
- App crashes
- High latency
"""

class WarRoomState(TypedDict):
    data_output: Dict[str, Any]
    marketing_output: Dict[str, Any]
    risk_output: Dict[str, Any]
    final_decision: Dict[str, Any]

async def data_node(state: WarRoomState):
    logger.info("Running Data Analyst Agent")
    result = await run_data_analyst_agent()
    logger.info(f"Data Analyst Output: {result}")
    return {"data_output": result}

async def marketing_node(state: WarRoomState):
    logger.info("Running Marketing Agent")
    result = await run_marketing_agent()
    logger.info(f"Marketing Output: {result}")
    return {"marketing_output": result}

async def risk_node(state: WarRoomState):
    logger.info("Running Risk Agent")
    result = await run_risk_agent()
    logger.info(f"Risk Output: {result}")
    return {"risk_output": result}

async def pm_node(state: WarRoomState):
    logger.info("Running PM Agent")
    result = await run_pm_agent(
        state["data_output"],
        state["marketing_output"],
        state["risk_output"],
        RELEASE_NOTES
    )
    logger.info(f"Final Decision: {result}")
    return {"final_decision": result}

def build_graph():
    graph = StateGraph(WarRoomState)

    graph.add_node("data", data_node)
    graph.add_node("marketing", marketing_node)
    graph.add_node("risk", risk_node)
    graph.add_node("pm", pm_node)

    graph.set_entry_point("data")

    graph.add_edge("data", "marketing")
    graph.add_edge("marketing", "risk")
    graph.add_edge("risk", "pm")
    graph.add_edge("pm", END)

    return graph.compile()

async def main():
    logger.info("WAR ROOM STARTED")
    graph = build_graph()
    result = await graph.ainvoke({})
    logger.info("WAR ROOM COMPLETED")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())