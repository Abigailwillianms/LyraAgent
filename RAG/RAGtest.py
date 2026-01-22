import os
from llama_index.indices.managed.dashscope import DashScopeCloudIndex

from dotenv import load_dotenv
load_dotenv()

os.environ["DASHSCOPE_API_KEY"] = "sk-73ec97ad5267482db39f3ce868bd6dcc"
os.environ["DASHSCOPE_WORKSPACE_ID"] = "llm-df9fs2iruwcayvy6"
if "DASHSCOPE_WORKSPACE_ID" not in os.environ or os.environ["DASHSCOPE_WORKSPACE_ID"] is None:
    raise ValueError("DASHSCOPE_WORKSPACE_ID 未设置，无法操作 DashScope Cloud Index。")

# 需要工作空间下存在名称为”my_first_index“的知识库
index = DashScopeCloudIndex("RAGTest")
print("完成云端知识库构建")

# 初始化检索引擎，retriever为DashScopeCloudRetriever类
retriever = index.as_retriever()
print("===========================================================================================================")
# 执行向量数据库检索
nodes = retriever.retrieve("你知道的阿里云百炼手机是什么吗？")
# 展示检索到的第一个TextNode向量
print(nodes[0])