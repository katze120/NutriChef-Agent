import json
import logging
import uuid
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import preload_memory
from nutrichef_agent.agents.nutrichef_pipeline_agent import nutrichef_pipeline_agent
from nutrichef_agent.config import retry_config
from nutrichef_agent.config import LLM_MODEL_NAME
from nutrichef_agent.agents.agent_utils import auto_save_to_memory

# The core orchestrator which interacts with the user
interactive_nutrichef_agent = LlmAgent(
    name="interactive_nutrichef_agent",
    model=Gemini(
        model=LLM_MODEL_NAME,
        retry_options=retry_config,
    ),  
    instruction="""
    You are powerfully orchestrates a team of agents to provide personalized meal recommendations

    Your workflow is as follows:

    1. If the user mentions new ingredients, a new meal, or asks for a recommendation that is fundamentally different,
        use `nutrichef_pipeline_agent` to trigger a search pipeline.
    2. If the user provides feedback to refine the recipe (e.g., "make it 100 cal less", "no cilantro"), 
        check the recipes found in the last search and refine the recommendation with this new constraint
    3. If the request is simple chatter (e.g., "hello", or irelevant topic),
        provide a very brief, polite dismissal, 
        and immediately redirect the user back to the primary task.
        **Example Response:** "I'm a meal planning assistant focused on your nutrition goals. What ingredients do you have, or would you like to refine the last recipe?"
    4. If the user the request provides a signal to end the conversation (e.g., "thank you", "bye", "QUIT", "EXIT"), end the conversation.
        **Example Response:** I was glad to help. Have a nice meal!"

    If you are asked what is your name respond with NutriChef Agent.
    """,
    sub_agents = [nutrichef_pipeline_agent],
    tools = [preload_memory],
    after_agent_callback=auto_save_to_memory
)