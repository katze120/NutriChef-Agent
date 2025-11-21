from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from nutrichef_agent.config import retry_config
from nutrichef_agent.config import LLM_MODEL_NAME
from nutrichef_agent.tools.spoonacular_tools import get_recipe_information

# It takes Recipe IDs and gets the hard nutritional facts.
nutritionist_agent = LlmAgent(
    name="nutritionist_agent",
    model=Gemini(
        model=LLM_MODEL_NAME,
        retry_options=retry_config
    ), 
    tools=[get_recipe_information],
    instruction="""
    You are a data analyst for food.
    1. You will receive a list of Recipe IDs.
        If you did not receive a valid list of Recipe IDs, do not call `get_recipe_information` tool and proceed with output.
    2. Extract the IDs and use the `get_recipe_information` tool to get the nutritional facts, for up to 5 Recipe IDs.
    3. Output the full JSON list of detailed nutritional data.

    OUTPUT RULES:
    1. You must return ONLY a valid JSON object.
    2. Do not include markdown formatting (no ```json or ```).
    3. Structure: {"status": [X], "enriched_data": [output_from_`get_recipe_information`_tool]}
    
    If you did not get any recipe IDs from previous agent or if there's error from the `search_recipes` tool, return `status` as `failed`.
    If everything is good, return `status` as `success`.
    """,
    output_key = "enriched_data"
)