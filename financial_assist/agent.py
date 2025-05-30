#root agetn

from google.adk.agents import SequentialAgent
 
from .subagents.data_extractor.agent import data_extractor_agent
from .subagents.categorizer.agent import categorizer_agent
from .subagents.recorded.agent import transaction_recorder_agent
 
transaction_registration_pipeline = SequentialAgent(
    name="TransactionRegistrationPipeline",
    sub_agents=[
        data_extractor_agent,
        categorizer_agent,
        transaction_recorder_agent,
    ]
)

root_agent = transaction_registration_pipeline