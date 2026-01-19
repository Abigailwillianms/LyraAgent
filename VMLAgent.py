from langchain.agents import create_agent
from loadModel import VML
from airtest.core.api import *
from AirtestTools import AgentTouch
from MemoryLoad import checkp,config
from GetWindowTitle import get_window_titles
from PIL import Image

# 获取窗口列表
window_list = get_window_titles()

print("请选择输入一个窗口标题或HWND：")
input_value = input()
while not input_value:
    input_value = input("未找到窗口，请重新输入一个窗口标题或HWND：")

# 确定要使用的窗口标题
Window = input_value
# 如果输入是数字，尝试作为HWND查找对应的标题
if input_value.isdigit():
    target_hwnd = int(input_value)
    for hwnd, title in window_list:
        if hwnd == target_hwnd:
            Window = title
            print(f"已通过HWND找到窗口：{title}")
            break

print("已找到窗口，请准备输入指令==========")



agent=create_agent(
    model=VML,
    tools=[AgentTouch],
    system_prompt="""你是一个拥有视觉的小助手，可以帮助我分析图像并实现点击操作，请记住“每次回答告诉我你的思考过程，以及调用了几次工具，每次传入的参数”。
    对于工具调用，请记住以下几点：
    1.调用AgentTouch时传递的坐标是x,y两个float类型,而非列表或元组；
    对于不同的窗口，请记住下面的一些操作流程：
    1.对于网易云音乐：播放音乐通过点击歌曲头像左侧的数字来播放
    2.对于qq音乐，播放音乐通过点击歌曲头像播放
    """,
    checkpointer=checkp,
)

#并且告诉我你的思考过程，以及调用了几次工具，每次传入的参数
step=0
while True:
    try:
        # 检查输入是否为数字（HWND）
        if Window.isdigit():
            # 通过HWND连接窗口
            connect_device(f"Windows:///?hwnd={Window}")
        else:
            # 通过窗口标题连接窗口
            connect_device(f"Windows:///?title_re={Window}*")
        window = device().app.top_window()  # 获取当前窗口
        break
    except Exception as e:
        print(f"连接窗口失败: {e}")
        Window = input("请重新输入一个有效的窗口标题或HWND：")
        if not Window:
            continue


while True:
    try:
        step=step+1
        Ins = input("请输入下一步指令：")
        window.set_focus()
        snapshot(f"./images/images{step}.jpg")
        img = Image.open(f"./images/images{step}.jpg")
        width, height = img.size
        #print(f"截图分辨率: {width}x{height}")
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": f"D:/_Git_Pro/LyraAgent/images/images{step}.jpg"},
                    {"text": Ins}]
            }]
        res = agent.invoke(
            {"messages": messages}
            , config
        )
        print(res['messages'][-1].content)
    except Exception as e:
        print(f"执行指令时出错: {e}")
        print("请重新输入指令或检查窗口状态。")
        # 减少step计数，避免截图文件序号跳跃
        step=step-1
        continue




"""sleep(2)
image = snapshot("./images/images02.jpg")
messages2 = [
{
    "role": "user",
    "content": [
    {"image": f"images/images02.jpg"},
    {"text": "请告诉我你第一步点击的坐标"}]
}]
res2=agent.invoke({"messages": messages2},config)
print(res2['messages'][-1].content)"""

#AI((496, 935)),,(97,490)，，(391, 45)，，(921, 420)
#AIR(663, 891),,(140, 463)，，(470, 45)，，(1225, 395)

"""
for step in agent.stream({"messages": messages}, stream_mode="values"):
    # 获取content内容
    content = step["messages"][-1].content
    text_fragments = []

    # 遍历content中的每个元素，兼容不同数据格式
    for item in content:
        # 情况1：元素是字典，尝试提取text键（容错处理）
        if isinstance(item, dict):
            # 优先取'text'，没有则取其他常见键，最后为空字符串
            text_fragments.append(item.get('text', item.get('content', item.get('value', ''))))


    # 拼接成完整文本并流式打印
    full_text = ''.join(text_fragments)
    print(full_text, end='', flush=True)"""