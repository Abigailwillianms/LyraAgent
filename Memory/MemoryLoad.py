from langgraph.checkpoint.memory import InMemorySaver
from llama_index.indices.managed.dashscope import DashScopeCloudIndex
import time

# 创建内存检查点保存器
checkp=InMemorySaver()

# 错误步骤记录系统
class ErrorRecorder:
    def __init__(self):
        self.error_steps = {}
        self.rag_index = DashScopeCloudIndex("RAGTest")
    
    def record_error(self, step, action, reason):
        """记录错误步骤
        
        Args:
            step: 当前步骤编号
            action: 执行的操作
            reason: 错误原因
        """
        if step not in self.error_steps:
            self.error_steps[step] = []
        error_info = {
            "action": action,
            "reason": reason,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        self.error_steps[step].append(error_info)
        
        # 上传错误信息到阿里云RAG知识库
        self.upload_error_to_rag(step, action, reason)
    
    def get_error_history(self, step):
        """获取指定步骤的错误历史
        
        Args:
            step: 步骤编号
            
        Returns:
            错误历史列表
        """
        return self.error_steps.get(step, [])
    
    def has_error(self, step, action):
        """检查指定步骤是否执行过相同的错误操作
        
        Args:
            step: 步骤编号
            action: 操作描述
            
        Returns:
            是否执行过相同的错误操作
        """
        if step not in self.error_steps:
            return False
        
        for error in self.error_steps[step]:
            if error["action"] == action:
                return True
        return False
    
    def upload_error_to_rag(self, step, action, reason):
        """上传错误信息到阿里云RAG知识库
        
        Args:
            step: 步骤编号
            action: 执行的操作
            reason: 错误原因
        """
        try:
            # 构建错误信息内容
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            error_content = f"错误信息：\n"
            error_content += f"步骤：{step}\n"
            error_content += f"时间：{timestamp}\n"
            error_content += f"操作：{action}\n"
            error_content += f"原因：{reason}\n"
            error_content += f"\n解决方案提示：请尝试不同的操作方法，避免重复相同的错误。"
            
            # 简化处理，暂时注释上传操作以避免API错误
            # 等待网络恢复后可以重新启用
            print(f"【错误上传准备】步骤 {step}：{action} - 错误信息已准备就绪")
            print(f"错误内容：{error_content}")
        except Exception as e:
            print(f"【知识库上传失败】上传错误信息失败：{str(e)}")
    
    def retrieve_error_from_rag(self, query):
        """从阿里云RAG知识库检索错误信息
        
        Args:
            query: 查询语句
            
        Returns:
            检索到的错误信息
        """
        try:
            retriever = self.rag_index.as_retriever()
            nodes = retriever.retrieve(query)
            if nodes:
                result = "从知识库检索到的相关错误信息：\n"
                for i, node in enumerate(nodes[:3]):  # 只返回前3个结果
                    result += f"{i+1}. {node.text}\n\n"
                return result
            return ""
        except Exception as e:
            print(f"【知识库检索失败】检索错误信息失败：{str(e)}")
            return ""

# 创建错误记录器实例
error_recorder = ErrorRecorder()

# 配置
config={
    "configurable":{
        "thread_id":"1",
    }
}