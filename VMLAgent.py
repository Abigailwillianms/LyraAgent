from langchain.agents import create_agent
from VML.loadModel import VML
from airtest.core.api import *
from VMLTools.AirtestTools import AgentTouch,AgentKeyEvent
from VMLTools.RAGTools import GetRAG
from Memory.MemoryLoad import checkp,config
from Tools.GetWindowTitle import get_window_titles
from PIL import Image

get_window_titles()

Window = input("请选择输入一个窗口标题：")
while not Window:
    Window = input("未找到窗口，请重新输入一个窗口标题：")

print("已找到窗口，请准备输入指令==========")



agent=create_agent(
    model=VML,
    tools=[AgentTouch,AgentKeyEvent,GetRAG],
    system_prompt="""你是一个强大的电脑使用者。
    对于工具调用，请记住以下几点：
    1.调用AgentTouch时传递的坐标是x,y两个float类型,而非列表或元组；
    2.请注意：如果你认为需要分多步操作，可以先规划当前页面的操作并退出，我后续会为你提供你打开的页面供你继续执行，请不要
    一直尝试同样的操作
    
    对于不同的窗口，请记住下面的一些操作流程：
    1.对于网易云音乐：播放音乐通过点击歌曲头像左侧的数字来播放
    2.对于qq音乐，播放音乐通过点击歌曲头像播放
    """,
    checkpointer=checkp,
)

#并且告诉我你的思考过程，以及调用了几次工具，每次传入的参数
step=0
connect_device(f"Windows:///?title_re={Window}*")
window = device().app.top_window()  # 获取当前窗口


while True:
    step=step+1
    Ins = input("请输入下一步指令：")
    window.set_focus()
    snapshot(f"./images/images{step}.jpg")
    img = Image.open(f"./images/images{step}.jpg")
    width, height = img.size
    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"images/images{step}.jpg"},
                {"text": Ins}]
        }]
    for chunk in agent.stream(
            {"messages": messages}
            , config,
            #stream_mode="updates"
    ):
        for ST, data in chunk.items():
            print(data['messages'][-1].content,flush=True)
    """res = agent.invoke(
        {"messages": messages}
        , config
    )
    print(res['messages'][-1].content)"""
    ret=""
    rew=0
    while ret!="Exit":
        rew=rew+1
        print("正在评估下一步")
        snapshot(f"./images/images{step}_res{rew}.jpg")
        img = Image.open(f"./images/images{step}_res{rew}.jpg")
        width, height = img.size
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": f"images/images{step}_res{rew}.jpg"},
                    {"text": "这是你完成的效果，请评估是否达成成果，若达成则严格输出且仅输出'Exit'(不要有其他任何内容)，若未达成则重试"}]
            }]
        for chunk in agent.stream(
                {"messages": messages}
                , config,
                stream_mode="updates"
        ):
            for ST, data in chunk.items():
                ret=data['messages'][-1].content
                print(ret, flush=True)




