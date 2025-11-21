from nutrichef_agent.agent import root_agent
from google.adk.agents import Agent
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.plugins import LoggingPlugin
from google.genai import types
from dotenv import load_dotenv
from nutrichef_agent.config import APP_NAME
import asyncio
import uuid

load_dotenv() 

USER_ID = "default"

# SQLite database will be created automatically
db_url = "sqlite:///nutrichef_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)
# ADK's built-in Memory Service for development and testing
memory_service = InMemoryMemoryService()

async def main():
    runner = Runner(
        agent=root_agent, 
        app_name=APP_NAME, 
        session_service=session_service, 
        memory_service=memory_service,
        plugins=[
            LoggingPlugin()
        ],
    )
    
    session_id = str(uuid.uuid4())

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    user_input = input("\nWhat's in your fridge and what are you looking for? (e.g., 'chicken, broccoli, onion, under 500 calories, 20 min')\n> ")
    while True:
        query_content = types.Content(role="user", parts=[types.Part(text=user_input)])
        async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=query_content):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")
        user_input = input("\n[You] ")

if __name__ == "__main__":
    asyncio.run(main())        