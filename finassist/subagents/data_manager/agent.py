from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types


from .transaction.agent import transaction_manager
from .account.agent import account_manager

from finassist.utils.utils import get_var_env
from .prompt import DATABASE_MANAGER_INSTRUCTION

DATABASE_MANAGER_MODEL = LiteLlm(get_var_env("DATABASE_MANAGER_MODEL"))


database_manager = LlmAgent(
    name="database_manager",
    model=DATABASE_MANAGER_MODEL,
    description="Routes database write operations to specialized agents",
    instruction=DATABASE_MANAGER_INSTRUCTION,
    sub_agents=[
        transaction_manager,
        account_manager,  # Assuming account_agent is defined elsewhere
        # Add other specialized agents here as they are implemented
        # account_manager,
        # budget_manager,
    ],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=500,
        temperature=0.2,
    )
)
