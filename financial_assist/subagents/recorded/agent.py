from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from financial_assist.utils.utils import get_env_var
from .prompts import recorded_prompt_instruction
from .tools import execute_sql_query
MODEL = LiteLlm(get_env_var("BASELINE_NL2SQL_MODEL"))

transaction_recorder_agent = LlmAgent(
    name="TransactionRecorderAgent",
    model=MODEL,
    description="Records transactions into the database using SQL queries.",
    instruction=recorded_prompt_instruction(),
    tools=[execute_sql_query],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,
    ),
    output_key="sql_query",   
)

root_agent = transaction_recorder_agent