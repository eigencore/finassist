from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from finassist.utils.utils import get_var_env
from .prompt import TRANSACTION_AGENT_PROMPT
from .tools import add_transaction

TRANSACTION_AGENT_MODEL = LiteLlm(get_var_env("TRANSACTION_AGENT_MODEL"))

transaction_agent = LlmAgent(
    name="transaction_agent",
    model=TRANSACTION_AGENT_MODEL,
    instruction=TRANSACTION_AGENT_PROMPT,
    description="This agent is responsible for processing and storing financial transactions.",
    tools=[add_transaction],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.2,
    )
)