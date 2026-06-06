from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """The state of the agent in the graph."""
    messages: Annotated[List[BaseMessage], operator.add]
    context: str
