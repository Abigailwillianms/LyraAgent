from VML.loadModel import VML
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware

summid =  ModelCallLimitMiddleware(
            thread_limit=10,  # 每个线程（跨多次运行）最多 10 次调用
            run_limit=5,  # 每次运行（单次调用）最多 5 次调用
            exit_behavior="end",  # 或者 "error" 以引发异常
        )
agent = create_agent(
    model=VML,
    tools=[],
    middleware=[
        summid
    ],
)
for chunk in agent.stream(
        {"messages": "hello"}
):
    for ST, data in chunk.items():
        print(data['messages'][-1].content, flush=True)