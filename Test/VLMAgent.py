from langchain.agents import create_agent
from VML.loadModel import VML

agent=create_agent(
    model=VML,
    tools=[],
    system_prompt="""你是一个拥有视觉的小助手，可以帮助我分析图像""",
)
messages = [
{
    "role": "user",
    "content": [
    {"image": "D:\\1\\新建文件夹\\Saved Pictures\\abigail.jpg"},
    {"text": "图中描绘的是什么景象?"}]
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