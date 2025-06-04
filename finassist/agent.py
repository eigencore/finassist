from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from .subagents.transaction.agent import transaction_agent
from .subagents.question.agent import question_agent

from finassist.utils.utils import get_var_env
from finassist.prompt import MAIN_AGENT_PROMPT

MAIN_AGENT_MODEL = LiteLlm(get_var_env("MAIN_AGENT_MODEL"))


root_agent = Agent(
    name="root_agent",
    model=MAIN_AGENT_MODEL,
    instruction=MAIN_AGENT_PROMPT,
    description="This is the main agent that orchestrates the financial tasks.",
    sub_agents=[
        transaction_agent,
        question_agent
    ],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=0.2,
    ),
)

    