import langchain
print(langchain.__version__)
from langchain.agents import create_agent
from VML.loadModel import VML

agent = create_agent(
    model= VML,
    tool=[],
)
print(agent)