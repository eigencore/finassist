from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from finassist.utils.utils import get_var_env
from finassist.utils.database import get_user_context_info
from .prompt import TRANSACTION_AGENT_PROMPT
from .tools import add_transaction

TRANSACTION_AGENT_MODEL = LiteLlm(get_var_env("TRANSACTION_AGENT_MODEL"))

def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Give context about the user to the agent."""
    try:
        # Obtener user_id del contexto real en lugar de hardcodearlo
        user_id = "user_001" # or callback_context.session_state.get("user_id") 
        if not user_id:
            # Fallback o manejo de error
            print("Warning: No user_id found in session state")
            return
            
        user_context = get_user_context_info(user_id)
        if not user_context:
            print(f"Warning: No context found for user {user_id}")
            return
            
        # Sanitización más robusta
        user_context = user_context.replace("{","{{").replace("}","}}") 
        
        # Validar que el agente existe
        if hasattr(callback_context._invocation_context, 'agent'):
            callback_context._invocation_context.agent.instruction = (
                TRANSACTION_AGENT_PROMPT +
                f"""
                ------ User Context ------
                {user_context}
                ---------------------------
                """
            )
        else:
            print("Error: Agent not found in callback context")
            
    except Exception as e:
        print(f"Error in before_agent_callback: {e}")
        # No modificar la instrucción si hay error
    

transaction_manager = LlmAgent(
    name="transaction_agent",
    model=TRANSACTION_AGENT_MODEL,
    instruction=TRANSACTION_AGENT_PROMPT,
    description="This agent is responsible for processing and storing financial transactions.",
    tools=[add_transaction],
    before_agent_callback=setup_before_agent_call,
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.2,
    )
)