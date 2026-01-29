from langchain.agents import create_agent
from VML.loadModel import VML
from airtest.core.api import *
from VMLTools.AirtestTools import AgentTouch, AgentKeyEvent
from VMLTools.GenshinTools import Genshin_move
from VMLTools.RAGTools import GetRAG
from Memory.MemoryLoad import checkp, config
from langchain.agents.middleware import SummarizationMiddleware, ToolCallLimitMiddleware,ModelCallLimitMiddleware

summarize_mid = SummarizationMiddleware(
            model=VML,
            max_tokens_before_summary=4000,
            messages_to_keep=20,
        )
modelLimiter = ModelCallLimitMiddleware(
            run_limit=3,
            exit_behavior="end",
        )
global_limiter = ToolCallLimitMiddleware(run_limit=3,exit_behavior="end")
RAG_limiter = ToolCallLimitMiddleware(
    tool_name="搜索知识库",
    run_limit=1,
)
Move_limiter = ToolCallLimitMiddleware(
    tool_name="角色移动",
    run_limit=1,
    exit_behavior="end"
)

def execute_agent_task(window, initial_instruction,nums):
    # 创建agent
    agent = create_agent(
        model=VML,
        tools=[AgentTouch, AgentKeyEvent, GetRAG, Genshin_move],
        system_prompt=f"""
            你是一名经验丰富的原神PC端玩家，擅长进行长时间的原神游玩。请根据当前游戏画面，规划接下来一步操作。
            请记住：
            1.如果你若评估任务已完成请返回以“Exit”的回答，这样可以触发结束操作；
            2.请准确严谨地判断是否完成任务，在输出的图像中看到任务完成之前绝对不能返回“Exit”。
            
            你目前需要完成的任务是{initial_instruction}。
            """,
        checkpointer=checkp,
        middleware=[modelLimiter,RAG_limiter,Move_limiter,summarize_mid]
    )

    # 初始化变量
    step = 0
    retry_count = 0

    while True:
        step += 1
        # 截图
        window.set_focus()
        snapshot(f"./images/images{nums}{step}.jpg")

        messages = [
            {
                "role": "user",
                "content": [
                    {"image": f"images/images{nums}{step}.jpg"},
                    {"text": f"第{step}步，我已为你提供更多的所有工具的调用次数，请继续完成{initial_instruction}任务，注意：若没有完成请务必继续执行"}
                ]
            }
        ]

        print(f"步骤 {step}：输入图片images{nums}{step}.jpg")

        res = agent.invoke(
            {"messages": messages}
            , config
        )
        ret = res['messages'][-1].content
        print(ret)
        if isinstance(ret, str):
            retry_count += 1
        else:
            ret=ret[0]['text']
            if ret.endswith("Exit"):
                return
            else:
                retry_count += 1




