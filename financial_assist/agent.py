import os
from datetime import date
from google.adk.agents import Agent

from .prompts import return_instructions_root

date_today = date.today()

def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "database_settings" not in callback_context.state:
        db_settings = dict()
        db_settings["use_database"] = "BigQuery"
        callback_context.state["all_db_settings"] = db_settings

    # setting up schema in instruction
    if callback_context.state["all_db_settings"]["use_database"] == "BigQuery":
        callback_context.state["database_settings"] = get_bq_database_settings()
        schema = callback_context.state["database_settings"]["bq_ddl_schema"]

        callback_context._invocation_context.agent.instruction = (
            return_instructions_root()
            + f"""

    --------- The BigQuery schema of the relevant data with a few sample rows. ---------
    {schema}

    """
        )

root_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="finassist_multiagent",
    instruction=return_instructions_root(),
    global_instruction=(
        f"""
        You are the FinAssit, an autonomous multi-agent system that acts as a personal or small business financial auditor.
        Todays date: {date_today}
        """
    )
)