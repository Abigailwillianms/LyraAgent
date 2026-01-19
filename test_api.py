import dashscope
from dotenv import load_dotenv
import os
import requests

load_dotenv()
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 测试网络连接
print("测试网络连接...")
try:
    response = requests.get("https://www.baidu.com", timeout=5)
    print(f"网络连接正常: {response.status_code}")
except Exception as e:
    print(f"网络连接失败: {e}")

# 测试DNS解析
print("\n测试DNS解析...")
try:
    import socket
    ip = socket.gethostbyname("dashscope.aliyuncs.com")
    print(f"DNS解析正常: dashscope.aliyuncs.com -> {ip}")
except Exception as e:
    print(f"DNS解析失败: {e}")

# 测试API密钥
print("\n测试API密钥...")
api_key = os.getenv("TONGYI_API_KEY2")
print(f"API密钥: {api_key}")

# 测试简单的文本生成
print("\n测试简单的文本生成...")
try:
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt='你是谁',
        api_key=api_key
    )
    print(f"文本生成成功: {response.output.text}")
except Exception as e:
    print(f"文本生成失败: {e}")