from langchain.agents import create_agent
from VML.loadModel import VML
from airtest.core.api import *
from VMLTools.AirtestTools import AgentTouch,AgentKeyEvent
from VMLTools.RAGTools import GetRAG
from Memory.MemoryLoad import checkp,config
from Tools.GetWindowTitle import get_window_titles
import re
from PIL import Image
from Tools.LargeRight import adminSr
from langchain.agents.middleware import SummarizationMiddleware, ToolCallLimitMiddleware,ModelCallLimitMiddleware


#Model call limits exceeded: run limit (5/5)
global_limiter = ToolCallLimitMiddleware(run_limit=10)
modelLimiter =  ModelCallLimitMiddleware(
            run_limit=20,
            exit_behavior="end",
        )

touch_limiter = ToolCallLimitMiddleware(
    tool_name="点击",
    run_limit=10,
)
Keyboard_limiter = ToolCallLimitMiddleware(
    tool_name="键盘输入",
    run_limit=10,
)
#adminSr()


get_window_titles()

Window = input("请选择输入一个窗口标题：")
while not Window:
    Window = input("未找到窗口，请重新输入一个窗口标题：")

print("已找到窗口，请准备输入指令==========")



agent=create_agent(
    model=VML,
    tools=[AgentTouch,AgentKeyEvent,GetRAG],
    system_prompt="""你是一个强大的电脑使用者。请根据每次得到的图片规划接下来的最多3次工具调用操作。
    对于工具调用，请记住以下几点：
    1.请注意：如果指令中提到不是第一步，则说明你已完成前置步骤，请接着继续完成
    2.如果发现没有工具调用额度了，什么都不要输出直接返回，我会给你新的工具调用次数
    
    对于不同的窗口，请记住下面的一些操作流程：
    1.对于网易云音乐：播放音乐通过点击歌曲头像左侧的数字来播放
    2.对于qq音乐，播放音乐通过点击歌曲头像播放
    """,
    checkpointer=checkp,
    middleware=[modelLimiter,touch_limiter,Keyboard_limiter,global_limiter]
)

step=0
connect_device(f"Windows:///?title_re={Window}*")

window = device().app.top_window()  # 获取当前窗口

current_step = 1

while True:
    Ins = input("请输入下一步指令：")
    window.set_focus()
    snapshot(f"./images/images{current_step}.jpg")

    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"images/images{current_step}.jpg"},
                {"text": Ins}
            ]
        }
    ]
    res = agent.invoke(
        {"messages": messages}
        , config
    )
    print(res['messages'][-1].content)
    current_step += 1
    ret = ""
    rew = 0
    while ret != 'Success':
        rew = rew + 1
        print("正在评估下一步")
        # 重新截图，使用新的步数
        snapshot(f"./images/images{current_step}_res{rew}.jpg")
        messages2 = [
            {
                "role": "user",
                "content": [
                    {"image": f"images/images{current_step}_res{rew}.jpg"},
                    {
                        "text": f"第{rew}步，我已为你提供更多的工具调用次数，请继续{Ins}，若未完成则重试，若已完成任务则仅输出“Success”（此时不要输出其他任何东西）"
                        }]
            }]
        ret_response = agent.invoke(
            {"messages": messages2}
            , config
        )
        ret = ret_response['messages'][-1].content
        print(ret)



