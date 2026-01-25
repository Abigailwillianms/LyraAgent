#!/usr/bin/env python3
"""
简单测试文件读取
"""

import os

print("开始测试文件读取...")

# 检查.env文件
env_path = './.env'
print(f"检查文件: {env_path}")
print(f"文件存在: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    print(f"文件大小: {os.path.getsize(env_path)} 字节")
    print(f"文件修改时间: {os.path.getmtime(env_path)}")
    
    # 尝试读取文件
    try:
        print("\n读取文件内容:")
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"共 {len(lines)} 行")
        for i, line in enumerate(lines, 1):
            print(f"{i}: {repr(line)}")
        
        # 检查是否包含阿里云相关变量
        print("\n检查阿里云相关变量:")
        for line in lines:
            line = line.strip()
            if 'ALIBABA' in line:
                print(f"找到: {line}")
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                print(f"  键: '{key}'")
                print(f"  值: '{value}'")
                
    except Exception as e:
        print(f"读取失败: {e}")

print("测试完成!")
