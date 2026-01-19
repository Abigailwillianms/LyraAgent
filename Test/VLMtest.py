import dashscope
from dotenv import load_dotenv
import os

load_dotenv()
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"
messages = [
{
    "role": "user",
    "content": [
    {"image": "C:\\Users\\herunze\\Pictures\\Screenshots\\R-C.jpg"},
    {"text": "图中描绘的是什么东西?"}]
}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key = os.getenv("TONGYI_API_KEY"),
    model = 'qwen3-vl-plus',  # 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages = messages
)
print(response.output.choices[0].message.content[0]["text"])