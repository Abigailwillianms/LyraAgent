from langchain.agents import create_agent
from loadModel import VML
from airtest.core.api import *

connect_device("Windows:///?title_re=Never Gonna Give You Up - Rick Astley*")

agent=create_agent(
    model=VML,
    tools=[],
    system_prompt="""你是一个拥有视觉的小助手，可以帮助我分析图像""",
)

image = snapshot("./images/GameShot.jpg")

messages = [
{
    "role": "user",
    "content": [
    {"image": f"images/GameShot.jpg"},
    {"text": "这是一张网易云音乐的截图，你能告诉我我想听老歌应该选第几个歌单吗"}]
}]

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
    print(full_text, end='', flush=True)