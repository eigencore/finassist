from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from finassist.utils.utils import get_var_env
from .prompt import QUESTION_AGENT_PROMPT


QUESTION_AGENT_MODEL = LiteLlm(get_var_env("QUESTION_AGENT_MODEL"))

question_agent = LlmAgent(
    name="question_agent",
    model=QUESTION_AGENT_MODEL,
    instruction=QUESTION_AGENT_PROMPT,
    description="This agent is responsible for answering questions about finances.",
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.5,
    )
)