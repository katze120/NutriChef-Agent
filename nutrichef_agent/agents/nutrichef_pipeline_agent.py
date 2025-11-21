import json
from google.adk.agents import SequentialAgent
from nutrichef_agent.agents.parser_agent import parser_agent
from nutrichef_agent.agents.finder_agent import finder_agent
from nutrichef_agent.agents.nutritionist_agent import nutritionist_agent
from nutrichef_agent.agents.finalizer_agent import finalizer_agent

# The core logic of NutriChef with a robust, four-step data flow.
nutrichef_pipeline_agent = SequentialAgent(
    name="nutrichef_pipeline_agent",
    description="Orchestrates a team of agents to provide personalized meal recommendations.",
    sub_agents=[parser_agent, finder_agent, nutritionist_agent, finalizer_agent]
)
