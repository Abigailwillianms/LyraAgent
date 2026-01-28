from langchain.agents import create_agent
from VML.loadModel import VML
from airtest.core.api import *
from VMLTools.AirtestTools import AgentTouch, AgentKeyEvent
from VMLTools.GenshinTools import Genshin_move
from VMLTools.RAGTools import GetRAG
from Memory.MemoryLoad import checkp, config
from PIL import Image
from Tools.GetWindowTitle import get_window_titles
from langchain.agents.middleware import SummarizationMiddleware, ToolCallLimitMiddleware,ModelCallLimitMiddleware


modelLimiter =  ModelCallLimitMiddleware(
            run_limit=5,
            exit_behavior="end",
        )

touch_limiter = ToolCallLimitMiddleware(
    tool_name="点击",
    run_limit=3,
)
Keyboard_limiter = ToolCallLimitMiddleware(
    tool_name="键盘输入",
    run_limit=3,
)
def execute_agent_task(window_title, initial_instruction,nums):
    """
    非交互式执行agent任务

    参数:
        window_title: 窗口标题
        initial_instruction: 初始指令
        max_retries: 最大重试次数
    """


    # 连接设备
    try:
        connect_device(f"Windows:///?title_re={window_title}*")
        window = device().app.top_window()  # 获取当前窗口
        window.set_focus()
    except Exception as e:
        print(f"连接窗口失败")

    # 创建agent
    agent = create_agent(
        model=VML,
        tools=[AgentTouch, AgentKeyEvent, GetRAG, Genshin_move],
        system_prompt="""你是一个强大的电脑使用者。请根据每次得到的图片规划接下来的最多3次工具调用操作。
            对于工具调用，请记住以下几点：
            1.请注意：如果指令中提到不是第一步，则说明你已完成前置步骤，请接着继续完成
            2.如果发现没有工具调用额度了，请返回，我会给你新的工具调用次数
            3.如果你发现已经完成任务，请直接返回“Exit”(不要有其他任何多余内容)，这样可以触发结束操作
            4.如果没有完成任务，哪怕你已经没有工具调用次数了也不能返回“Exit”

            对于不同的窗口，请记住下面的一些操作流程：
            1.对于网易云音乐：播放音乐通过点击歌曲头像左侧的数字来播放
            2.搜索时，搜索框输入后可以键盘输入{ENTER}搜索
            """,
        checkpointer=checkp,
        middleware=[modelLimiter, touch_limiter, Keyboard_limiter]
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
                    {"text": initial_instruction}
                ]
            }
        ]

        print(f"步骤 {step}")

        res = agent.invoke(
            {"messages": messages}
            , config
        )
        ret = res['messages'][-1].content

        if isinstance(ret, str):
            retry_count += 1
        else:
            ret=ret[0]['text']
            print(ret)
            if ret == "Exit":
                print("正常退出")
                return
            else:
                retry_count += 1




