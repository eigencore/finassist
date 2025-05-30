from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types


from financial_assist.utils.utils import get_env_var
from financial_assist.subagents.bigquery.tools import get_user_categories
from .prompts import categorizer_agent_instruction
from .tools import (
    create_category,
    create_subcategory
)

CATEGORIZER_MODEL = LiteLlm(get_env_var("CATEGORIZER_MODEL"))

user_categories = get_user_categories(user_id="user_001")


categorizer_agent = LlmAgent(
    name = "CategorizerAgent",
    model=CATEGORIZER_MODEL,
    description = "Categorizes transactions into user-defined categories and subcategories if available. If not, suggests new categories or subcategories.",
    instruction=categorizer_agent_instruction(user_categories),
    #tools=[create_category, create_subcategory],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
    ),
    output_key="categorized_transaction",
)
    
    
    
    