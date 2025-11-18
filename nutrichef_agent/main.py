from nutrichef_agent.agents.root_agent import nutrichef_agent
from google.adk.runners import InMemoryRunner
import asyncio
import os
from dotenv import load_dotenv

load_dotenv() 

async def main():
    runner = InMemoryRunner(agent=nutrichef_agent)
    print("✅ ADK Runner created for NutriChef Agent.")

    user_input = input("\nWhat's in your fridge and what are you looking for? (e.g., 'chicken, broccoli, onion, under 500 calories, 20 min')\n> ")
        
    response = await runner.run_debug(user_input)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())        