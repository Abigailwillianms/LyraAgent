import os
import dashscope
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv

load_dotenv()
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"
class VMLTongyi(ChatTongyi):
    def GetImage(self,message):

        response = dashscope.MultiModalConversation.call(
            api_key=os.getenv("TONGYI_API_KEY"),
            model='qwen3-vl-plus',
            messages=messages
        )
        print(response.output.choices[0].message.content[0]["text"])
VML = VMLTongyi(
    api_key=os.getenv("TONGYI_API_KEY"),
    model='qwen3-vl-plus',
)

messages = [
{
    "role": "user",
    "content": [
    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
    {"text": "图中描绘的是什么景象?"}]
}]

#VML.GetImage(messages)


