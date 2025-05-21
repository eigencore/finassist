# agent/agent.py
import os
import datetime
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from .prompts import master_agent_instruction
from .subagents.parser_agent.agent import parser_agent as call_parser_agent
from .tools import crud_service_tool as execute_crud_operation

MODEL = os.getenv("MASTER_MODEL")


master_agent = LlmAgent(
    name="master_agent",
    model=LiteLlm(MODEL),
    description="A master agent that orchestrates financial operations by coordinating parser and database agents.",
    instruction=master_agent_instruction(),
    tools=[
        AgentTool(agent=call_parser_agent),
        execute_crud_operation,
    ]
)

root_agent = master_agent