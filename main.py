import asyncio
import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from agents.data_analyst_agent import run_data_analyst_agent
from agents.marketing_agent import run_marketing_agent
from agents.risk_agent import run_risk_agent
from agents.product_manager_agent import run_pm_agent
import os
file_path = os.path.join(os.path.dirname(__file__), 'data', 'release_notes.txt')

logging.basicConfig(
    filename="war_room.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)
with open(file_path, 'r', encoding='utf-8') as file:
    RELEASE_NOTES = file.read().strip()

class WarRoomState(TypedDict):
    data_output: Dict[str, Any]
    marketing_output: Dict[str, Any]
    risk_output: Dict[str, Any]
    final_decision: Dict[str, Any]

def make_json_safe(data):
    if data is None:
        return None
    if isinstance(data, (str, int, float, bool)):
        return data
    if isinstance(data, dict):
        return {k: make_json_safe(v) for k, v in data.items()}
    if isinstance(data, (list, tuple, set)):
        return [make_json_safe(item) for item in data]
    if hasattr(data, "model_dump"):
        return make_json_safe(data.model_dump())
    if isinstance(data, datetime):
        return data.isoformat()
    if hasattr(data, "__dict__"):
        return make_json_safe(vars(data))
    return str(data)

def create_output_folder() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"war_room_output_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    logger.info(f"Created output folder: {folder_name}")
    return folder_name

async def save_output(folder: str, filename: str, data: Any):
    filepath = os.path.join(folder, filename)
    try:
        safe_data = make_json_safe(data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(safe_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved: {filepath}")
    except Exception as e:
        logger.error(f"Failed to save {filepath}: {e}")

async def data_node(state: WarRoomState):
    logger.info("Running Data Analyst Agent")
    result = await run_data_analyst_agent()
    logger.info(f"Data Analyst Output Type: {type(result)}")
    return {"data_output": make_json_safe(result)}

async def marketing_node(state: WarRoomState):
    logger.info("Running Marketing Agent")
    result = await run_marketing_agent()
    return {"marketing_output": make_json_safe(result)}

async def risk_node(state: WarRoomState):
    logger.info("Running Risk Agent")
    result = await run_risk_agent()
    return {"risk_output": make_json_safe(result)}

async def pm_node(state: WarRoomState):
    logger.info("Running PM Agent")
    result = await run_pm_agent(
        state["data_output"],
        state["marketing_output"],
        state["risk_output"],
        RELEASE_NOTES
    )
    return {"final_decision": make_json_safe(result)}

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
    
    output_folder = create_output_folder()
    
    graph = build_graph()
    result = await graph.ainvoke({})

    await save_output(output_folder, "data_analyst_output.json", result.get("data_output"))
    await save_output(output_folder, "marketing_output.json", result.get("marketing_output"))
    await save_output(output_folder, "risk_output.json", result.get("risk_output"))
    await save_output(output_folder, "final_decision.json", result.get("final_decision"))
    await save_output(output_folder, "war_room_complete_result.json", result)

    logger.info("WAR ROOM COMPLETED")
    print(f"War Room completed! All outputs saved in folder: {output_folder}")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())