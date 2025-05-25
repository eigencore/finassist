
import os
import datetime
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.callback_context import CallbackContext

from .prompts import transaction_agent_prompt
from .subagents.bigquery.tools import get_user_context
from .tools import execute_sql

MODEL = os.getenv("MASTER_MODEL")

# Cache global para el contexto del usuario
_user_context_cache = {}

def setup_user_context(callback_context: CallbackContext):
    """Setup user context for the agent with caching."""
    
    user_id = "user_001"  # O extraerlo del contexto
    
    # Verificar si ya tenemos el contexto en cache
    if user_id not in _user_context_cache:
        print(f"Loading user context for {user_id} (first time)")
        user_context = get_user_context(user_id=user_id)
        _user_context_cache[user_id] = user_context
    else:
        print(f"Using cached user context for {user_id}")
        user_context = _user_context_cache[user_id]
    
    user_context = user_context.replace('{', '{{').replace('}', '}}')
    
    callback_context._invocation_context.agent.instruction = (
        transaction_agent_prompt()
        + f"""

    --------- The user context and current date ---------
    {user_context}

    """
    )

master_agent = LlmAgent(
    name="master_agent",
    model=LiteLlm(MODEL),
    description="A master agent that orchestrates financial operations by coordinating parser and database agents.",
    instruction=transaction_agent_prompt(),
    before_agent_callback=setup_user_context,
    tools=[
        execute_sql,
    ]
)

root_agent = master_agent