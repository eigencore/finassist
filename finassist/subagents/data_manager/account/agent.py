from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from finassist.utils.utils import get_var_env
from .prompt import ACCOUNT_AGENT_PROMPT
from .tools import add_account

ACCOUNT_AGENT_MODEL = LiteLlm(get_var_env("ACCOUNT_AGENT_MODEL"))


def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Give context about the user to the agent."""
    try:
        # Obtener user_id del contexto real en lugar de hardcodearlo
        user_id = "user_001" # or callback_context.session_state.get("user_id") 
        if not user_id:
            # Fallback o manejo de error
            print("Warning: No user_id found in session state")
            return
            
        user_id = "user_001"  # Replace with actual user ID retrieval logic
        if not user_id:
            print(f"Warning: No user id: {user_id}")
            return
        # Validar que el agente existe
        if hasattr(callback_context._invocation_context, 'agent'):
            callback_context._invocation_context.agent.instruction = (
                ACCOUNT_AGENT_PROMPT +
                f"""
                ------ User Context ------
                user_id = {user_id}
                ---------------------------
                """
            )
        else:
            print("Error: Agent not found in callback context")
            
    except Exception as e:
        print(f"Error in before_agent_callback: {e}")
        # No modificar la instrucción si hay error

account_manager = LlmAgent(
    name="transaction_agent",
    model=ACCOUNT_AGENT_MODEL,
    instruction=ACCOUNT_AGENT_PROMPT,
    description="This agent is responsible for processing and storing financial transactions.",
    tools=[add_account],
    before_agent_callback=setup_before_agent_call,
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.2,
    )
)