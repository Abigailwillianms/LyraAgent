#!/usr/bin/env python3
"""
测试阿里云百炼知识库脚本
"""

import os
import sys
from dotenv import load_dotenv

print("开始执行测试脚本...")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")
print(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("加载环境变量...")
load_dotenv()
print("环境变量加载完成")

# 检查环境变量
print("检查环境变量...")
required_env_vars = [
    'ALIBABA_CLOUD_ACCESS_KEY_ID',
    'ALIBABA_CLOUD_ACCESS_KEY_SECRET',
    'DASHSCOPE_API_KEY'
]

print("当前环境变量值:")
for var in required_env_vars:
    value = os.getenv(var)
    if value:
        print(f"  {var}: 已设置 (长度: {len(value)})")
    else:
        print(f"  {var}: 未设置")

# 检查阿里云SDK是否安装
print("\n检查阿里云SDK...")
try:
    from alibabacloud_bailian20231229 import models
    from alibabacloud_bailian20231229.client import Client
    from alibabacloud_tea_openapi import models as open_api_models
    print("✅ 阿里云SDK已安装")
except ImportError as e:
    print(f"❌ 未安装阿里云SDK: {str(e)}")
    print("请运行: pip install alibabacloud-bailian20231229")

print("\n测试完成!")
