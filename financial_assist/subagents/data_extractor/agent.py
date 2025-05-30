from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from financial_assist.utils.utils import get_env_var
from financial_assist.subagents.bigquery.tools import get_user_context
from .prompt import data_extractor_instruction

DATA_EXTRACTOR_MODEL = LiteLlm(get_env_var("DATA_EXTRACTOR_MODEL"))

user_context = get_user_context(user_id="user_001")

data_extractor_agent = LlmAgent(
    name="DataExtractorAgent",
    model=DATA_EXTRACTOR_MODEL,
    description="Extracts structured transaction data from natural language inputs.",
    instruction=data_extractor_instruction(user_context),
    output_key="extracted_data",
)    

