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

"""Financial Assistant multi-agent system using Agent Development Kit"""

import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.readonly_context import ReadonlyContext
from finassist import prompt
from finassist.sub_agents.transaction.agent import transaction_agent
from finassist.sub_agents.consulting.agent import consulting_agent

from finassist.utils.utils import get_env_var

ROOT_AGENT_MODEL = LiteLlm(get_env_var("ROOT_AGENT_MODEL"))


def root_instruction_provider(context: ReadonlyContext) -> str:
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
    instruction = prompt.ROOT_AGENT_INSTR.replace("{_time}", current_time)
    instruction = instruction.replace("{user_profile}", str(user_profile))
    
    return instruction


root_agent = Agent(
    model=ROOT_AGENT_MODEL,
    name="root_agent",
    description="A Financial Assistant that manages transactions and provides educational financial guidance using specialized sub-agents",
    instruction=root_instruction_provider,
    sub_agents=[
        transaction_agent,
        consulting_agent,
    ],
) 