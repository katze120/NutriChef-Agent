import json
from google.adk.agents import SequentialAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import AgentTool, FunctionTool
from nutrichef_agent.agents.parser_agent import parser_agent
from nutrichef_agent.agents.finder_agent import finder_agent
from nutrichef_agent.agents.nutritionist_agent import nutritionist_agent
from nutrichef_agent.agents.finalizer_agent import finalizer_agent

nutrichef_pipeline_agent = SequentialAgent(
    name="nutrichef_pipeline_agent",
    description="Orchestrates a team of agents to provide personalized meal recommendations.",
    sub_agents=[parser_agent, finder_agent, nutritionist_agent, finalizer_agent]
)
