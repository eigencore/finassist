import os
import datetime
import json
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .prompts import parser_agent_instruction
from financial_assist.subagents.bigquery.tools import get_user_context
MODEL = os.getenv("PARSER_MODEL")

current_date = datetime.datetime.now().strftime("%Y-%m-%d")


def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent with updated context before each call."""
    
    user_context = get_user_context(user_id="user_001") # hardcoded for user ID
    
    user_context = user_context.replace('{', '{{').replace('}', '}}')
    
    callback_context._invocation_context.agent.instruction = (
        parser_agent_instruction()
        + f"""

--------- The User Context ---------
{user_context}

current_date: {current_date}
"""
    )

# Create the parser agent with the proper configuration
parser_agent = LlmAgent(
    name="call_parser_agent",
    model=LiteLlm(MODEL),
    description="A specialized agent that parses financial information from natural language into structured data.",
    instruction=parser_agent_instruction(),  
    tools=[], 
    before_agent_callback=setup_before_agent_call, 
    include_contents='default',
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,  
    )
)