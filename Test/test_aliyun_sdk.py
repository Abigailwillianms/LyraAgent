#!/usr/bin/env python3
"""
测试阿里云百炼SDK的可用方法
"""

import sys
print("测试阿里云百炼SDK...")

try:
    from alibabacloud_bailian20231229 import models
    from alibabacloud_bailian20231229.client import Client
    from alibabacloud_tea_openapi import models as open_api_models
    
    print("✅ 成功导入SDK")
    print(f"\nmodels模块内容:")
    
    # 查看models模块的所有属性
    model_attrs = [attr for attr in dir(models) if not attr.startswith('_')]
    print(f"models模块有 {len(model_attrs)} 个属性:")
    for attr in model_attrs[:20]:  # 只显示前20个
        print(f"  - {attr}")
    
    if len(model_attrs) > 20:
        print(f"  ... 还有 {len(model_attrs) - 20} 个属性")
    
    # 检查是否有与知识库相关的方法
    print("\n查找与知识库相关的方法:")
    for attr in model_attrs:
        if 'Knowledge' in attr or 'Doc' in attr or 'Base' in attr:
            print(f"  - {attr}")
    
    # 检查客户端方法
    print("\n客户端方法:")
    client_methods = [method for method in dir(Client) if not method.startswith('_')]
    print(f"Client类有 {len(client_methods)} 个方法:")
    for method in client_methods[:20]:
        print(f"  - {method}")
    
    if len(client_methods) > 20:
        print(f"  ... 还有 {len(client_methods) - 20} 个方法")
    
    # 查找与创建相关的方法
    print("\n查找与创建相关的方法:")
    for method in client_methods:
        if 'Create' in method or 'create' in method:
            print(f"  - {method}")
    
    print("\n测试完成!")

except Exception as e:
    print(f"❌ 测试出错: {str(e)}")
    import traceback
    traceback.print_exc()
