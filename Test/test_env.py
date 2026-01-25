#!/usr/bin/env python3
"""
详细测试环境变量加载问题
"""

import os
import sys
from dotenv import load_dotenv

print("开始执行环境变量测试脚本...")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")
print(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")

# 检查.env文件是否存在
env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
print(f"\n检查.env文件:")
print(f".env文件路径: {env_file_path}")
if os.path.exists(env_file_path):
    print("✅ .env文件存在")
    # 读取文件内容
    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"文件大小: {len(content)} 字节")
        print("文件内容:")
        print(content)
    except Exception as e:
        print(f"❌ 读取.env文件失败: {str(e)}")
else:
    print("❌ .env文件不存在")

# 检查当前环境中是否已有这些变量
print("\n检查系统环境变量:")
sys_vars = {
    'ALIBABA_CLOUD_ACCESS_KEY_ID': os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    'ALIBABA_CLOUD_ACCESS_KEY_SECRET': os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    'DASHSCOPE_API_KEY': os.environ.get('DASHSCOPE_API_KEY')
}

for var, value in sys_vars.items():
    if value:
        print(f"  {var}: 已设置 (系统环境变量)")
    else:
        print(f"  {var}: 未设置 (系统环境变量)")

# 测试dotenv加载
print("\n测试dotenv加载:")
try:
    # 显式指定.env文件路径
    load_result = load_dotenv(dotenv_path=env_file_path, override=True)
    print(f"load_dotenv返回值: {load_result}")
    print("加载后的值:")
    for var in sys_vars.keys():
        value = os.getenv(var)
        if value:
            print(f"  {var}: 已设置 (长度: {len(value)})")
        else:
            print(f"  {var}: 未设置")
except Exception as e:
    print(f"❌ dotenv加载失败: {str(e)}")

# 测试不同的加载方式
print("\n测试不同的加载方式:")
try:
    # 清除之前的环境变量
    for var in sys_vars.keys():
        if var in os.environ:
            del os.environ[var]
    print("已清除环境变量")
    
    # 方式1: 不指定路径
    print("\n方式1: 不指定路径")
    load_result1 = load_dotenv(override=True)
    print(f"load_dotenv返回值: {load_result1}")
    for var in sys_vars.keys():
        value = os.getenv(var)
        if value:
            print(f"  {var}: 已设置")
        else:
            print(f"  {var}: 未设置")
    
    # 方式2: 使用当前目录
    print("\n方式2: 使用当前目录的.env")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"切换到目录: {os.getcwd()}")
    load_result2 = load_dotenv(override=True)
    print(f"load_dotenv返回值: {load_result2}")
    for var in sys_vars.keys():
        value = os.getenv(var)
        if value:
            print(f"  {var}: 已设置")
        else:
            print(f"  {var}: 未设置")
            
except Exception as e:
    print(f"❌ 测试过程中出错: {str(e)}")

print("\n测试完成!")
