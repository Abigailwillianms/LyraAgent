#!/usr/bin/env python3
"""
创建阿里云百炼知识库的独立脚本
"""

import os
import sys
from dotenv import load_dotenv

print("开始执行脚本...")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("加载环境变量...")
load_dotenv()
print("环境变量加载完成")

# 检查环境变量
print("检查环境变量...")
required_env_vars = [
    'ALIBABA_CLOUD_ACCESS_KEY_ID',
    'ALIBABA_CLOUD_ACCESS_KEY_SECRET'
]

print("当前环境变量值:")
for var in required_env_vars:
    value = os.getenv(var)
    if value:
        print(f"  {var}: 已设置 (长度: {len(value)})")
    else:
        print(f"  {var}: 未设置")

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print("\n❌ 缺少必要的环境变量:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\n请在 .env 文件中添加以下变量:")
    print("ALIBABA_CLOUD_ACCESS_KEY_ID = 你的阿里云访问密钥ID")
    print("ALIBABA_CLOUD_ACCESS_KEY_SECRET = 你的阿里云访问密钥密钥")
    print("\n获取方式:")
    print("1. 登录阿里云控制台")
    print("2. 进入 'RAM 访问控制' -> '用户' -> '创建用户'")
    print("3. 为用户添加 'BailianFullAccess' 权限")
    print("4. 创建并下载访问密钥")
    sys.exit(1)

print("环境变量检查通过")

print("检查阿里云SDK...")
try:
    from alibabacloud_bailian20231229 import models
    from alibabacloud_bailian20231229.client import Client
    from alibabacloud_tea_openapi import models as open_api_models
    print("✅ 阿里云SDK已安装")
except ImportError:
    print("❌ 未安装阿里云百炼SDK")
    print("请运行: pip install alibabacloud-bailian20231229")
    sys.exit(1)

def create_bailian_client():
    """创建阿里云百炼客户端"""
    access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    region = os.getenv('ALIBABA_CLOUD_REGION', 'cn-beijing')
    
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=f'bailian.{region}.aliyuncs.com'
    )
    return Client(config)

def create_knowledge_base():
    """创建知识库"""
    print("\n" + "="*50)
    print("创建阿里云百炼知识库")
    print("="*50)
    
    # 获取必要参数
    workspace_id = input("请输入工作空间ID (Workspace ID): ").strip()
    if not workspace_id:
        print("❌ 工作空间ID不能为空")
        return None
    
    name = input("请输入知识库名称: ").strip()
    if not name:
        print("❌ 知识库名称不能为空")
        return None
    
    description = input("请输入知识库描述（可选）: ").strip()
    
    try:
        client = create_bailian_client()
        
        # 创建索引请求
        request = models.CreateIndexRequest(
            name=name,
            description=description,
            structure_type='vector',
            sink_type='vector_db'
        )
        
        # 发送创建请求
        response = client.create_index(workspace_id, request)
        
        if response.body.code == '200' and response.body.data:
            index_id = response.body.data.index_id
            print(f"\n✅ 知识库创建成功!")
            print(f"📋 知识库名称: {name}")
            print(f"🔑 知识库ID: {index_id}")
            print(f"📝 描述: {description}")
            
            print("\n� 使用方式:")
            print(f'  在代码中修改为:')
            print(f'  index = DashScopeCloudIndex("{index_id}")')
            print(f'  或')
            print(f'  self.rag_index = DashScopeCloudIndex("{index_id}")')
            
            return index_id
        else:
            print(f"❌ 知识库创建失败: {response.body.message}")
            return None
            
    except Exception as e:
        print(f"❌ 创建知识库时出错: {str(e)}")
        # 打印详细的错误信息
        import traceback
        traceback.print_exc()
        return None

def list_knowledge_bases():
    """列出所有知识库"""
    try:
        workspace_id = input("请输入工作空间ID (Workspace ID): ").strip()
        if not workspace_id:
            print("❌ 工作空间ID不能为空")
            return
            
        client = create_bailian_client()
        
        # 发送列表请求
        response = client.list_indexes(workspace_id)
        
        if response.body.code == '200':
            indexes = response.body.data.indexes
            if not indexes:
                print("📭 没有找到知识库")
                return
            
            print("\n📚 知识库列表:")
            print("="*60)
            for i, index in enumerate(indexes, 1):
                print(f"{i}. 名称: {index.name}")
                print(f"   ID: {index.index_id}")
                print(f"   描述: {index.description}")
                print(f"   类型: {index.type}")
                print(f"   状态: {index.status}")
                print(f"   创建时间: {index.create_time}")
                print("-"*40)
        else:
            print(f"❌ 获取知识库列表失败: {response.body.message}")
            
    except Exception as e:
        print(f"❌ 获取知识库列表时出错: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("\n阿里云百炼知识库管理工具")
    print("="*50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建知识库")
        print("2. 列出知识库")
        print("3. 退出")
        
        choice = input("\n请输入选项 (1-3): ").strip()
        
        if choice == '1':
            create_knowledge_base()
        elif choice == '2':
            list_knowledge_bases()
        elif choice == '3':
            print("退出程序")
            break
        else:
            print("❌ 无效选项")
        
        if choice != '3':
            input("\n按 Enter 键继续...")

if __name__ == "__main__":
    main()