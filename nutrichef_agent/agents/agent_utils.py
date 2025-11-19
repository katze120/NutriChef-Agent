
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.plugins.logging_plugin import  LoggingPlugin
from google.genai import types

APP_NAME="NUTRICHEF_AGENT"
USER_ID="default"

async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

async def run_session(
    runner: Runner,
    session_service: DatabaseSessionService,
    memory_service: InMemoryMemoryService,
    session_id: str,
    query: str
) -> str:
    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    # Convert the query string to the ADK Content format
    user_content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_content = "No final response received."
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    return final_response_content    