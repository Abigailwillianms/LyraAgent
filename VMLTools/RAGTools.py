from llama_index.indices.managed.dashscope import DashScopeCloudIndex
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool("搜索知识库",description="""本工具用于调用原神相关操作的知识库，参数query：需要查询的问题""")
def GetRAG(query:str) ->str:
    index = DashScopeCloudIndex("RAGTest")
    # 初始化检索引擎，retriever为DashScopeCloudRetriever类
    retriever = index.as_retriever()
    print("查询中===========================================================================================================")
    # 执行向量数据库检索
    nodes = retriever.retrieve(query)
    # 展示检索到的第一个TextNode向量
    return nodes[0]