from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from nutrichef_agent.config import retry_config
from nutrichef_agent.config import LLM_MODEL_NAME

# It takes messy text and extracts ingredients and constraints.
parser_agent = LlmAgent(
    name="parser_agent",
    model=Gemini(
        model=LLM_MODEL_NAME,
        retry_options=retry_config
    ),    
    instruction="""
    You are a Parser Agent for a nutrition app. 
    Your job is to extract ingredients and constraints from natural language.
    Example Input: "I have chicken and broccoli, need something under 500 calories, under 20 mins."
        
    OUTPUT RULES:
    1. You must return ONLY a valid JSON object.
    2. Do not include markdown formatting (no ```json or ```).
    3. Structure: {"ingredients": ["chicken", "broccoli"], "constraints": ["under 500 cal", "20 mins"]}
    4. If the user mentions a calorie limit, format it in constraints as 'max_calories: X'.
    """,
    output_key="parsed_constraints"
)