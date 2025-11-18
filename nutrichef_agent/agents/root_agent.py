import json
from google.adk.agents import SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool
from nutrichef_agent.agents.parser_agent import parser_agent
from nutrichef_agent.agents.finder_agent import finder_agent
from nutrichef_agent.agents.nutritionist_agent import nutritionist_agent
from nutrichef_agent.agents.finalizer_agent import finalizer_agent
from nutrichef_agent.config import retry_config
from nutrichef_agent.config import LLM_MODEL_NAME
#from .sub_agents.parser_agent import ParserAgent
#from .sub_agents.finder_agent import FinderAgent
#from .sub_agents.nutritionist_agent import NutritionistAgent

nutrichef_agent = SequentialAgent(
    name="nutrichef_agent",
    description="Orchestrates a team of agents to provide personalized meal recommendations.",
    sub_agents=[parser_agent, finder_agent, nutritionist_agent, finalizer_agent]
)
