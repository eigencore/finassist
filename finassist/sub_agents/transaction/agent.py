# Copyright 2025 Financial Assistant
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transaction agent for processing financial transactions."""

import datetime
from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.readonly_context import ReadonlyContext

from finassist.sub_agents.transaction import prompt
from finassist.sub_agents.transaction.tools import (
    extract_transaction_data_tool,
    generate_transaction_id_tool,
    get_current_timestamp_tool,
    format_transaction_summary_tool,
    validate_transaction_completeness_tool
)
from finassist.tools.categorization import categorize_transaction_tool
from finassist.tools.validation import (
    validate_currency_tool,
    validate_amount_tool,
    validate_date_tool,
    validate_payment_method_tool,
    save_transaction_tool
)

from finassist.utils.utils import get_env_var

TRANSACTION_AGENT_MODEL = LiteLlm(get_env_var("TRANSACTION_AGENT_MODEL"))


def transaction_instruction_provider(context: ReadonlyContext) -> str:
    """Provides dynamic instruction content with resolved context variables."""
    # Get current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get user profile from state (if available)
    user_profile = context.state.get("user:profile", "No profile information available")
    if isinstance(user_profile, dict):
        # Format profile dictionary as a readable string
        profile_items = [f"{k}: {v}" for k, v in user_profile.items()]
        user_profile = ", ".join(profile_items)
    
    # Replace template variables in the instruction
    instruction = prompt.TRANSACTION_AGENT_INSTR.replace("{_time}", current_time)
    instruction = instruction.replace("{user_profile}", str(user_profile))
    
    return instruction


transaction_agent = Agent(
    model=TRANSACTION_AGENT_MODEL,
    name="transaction_agent",
    description="Specialized agent for collecting and processing financial transaction information through natural conversation",
    instruction=transaction_instruction_provider,
    tools=[
        # Data extraction tools
        extract_transaction_data_tool,
        
        # Categorization tools
        categorize_transaction_tool,
        
        # Validation tools
        validate_currency_tool,
        validate_amount_tool,
        validate_date_tool,
        validate_payment_method_tool,
        
        # Transaction-specific tools
        generate_transaction_id_tool,
        get_current_timestamp_tool,
        format_transaction_summary_tool,
        validate_transaction_completeness_tool,
        
        # Save transaction tool
        save_transaction_tool,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,  # Lower temperature for more consistent data collection
        top_p=0.8
    )
) 