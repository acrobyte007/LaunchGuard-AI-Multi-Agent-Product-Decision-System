
from tools.feedback_scoring import semantic_feedback
import asyncio

async def main():
    feedback_input = r"data\Feedback.xlsx"
    result = await semantic_feedback(feedback_input)
    print(result)

asyncio.run(main())
