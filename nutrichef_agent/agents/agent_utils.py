
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