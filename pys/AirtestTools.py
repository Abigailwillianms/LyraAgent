from langchain_core.tools import tool
from airtest.core.api import *

@tool
def AgentTouch():
    touch()