#!/usr/bin/env python3
"""
测试Client.create_index方法的正确调用方式
"""

import sys
print("测试Client.create_index方法...")

try:
    from alibabacloud_bailian20231229 import models
    from alibabacloud_bailian20231229.client import Client
    from alibabacloud_tea_openapi import models as open_api_models
    
    print("✅ 成功导入模块")
    
    # 检查Client类的create_index方法
    print("\n检查Client.create_index方法:")
    import inspect
    if hasattr(Client, 'create_index'):
        print("✅ 找到create_index方法")
        # 获取方法签名
        sig = inspect.signature(Client.create_index)
        print(f"方法签名: {sig}")
        
        # 检查方法文档
        if Client.create_index.__doc__:
            print("\n方法文档:")
            print(Client.create_index.__doc__[:500] + "..." if len(Client.create_index.__doc__) > 500 else Client.create_index.__doc__)
    else:
        print("❌ 未找到create_index方法")
    
    # 检查所有以create开头的方法
    print("\n检查所有以create开头的方法:")
    create_methods = [method for method in dir(Client) if method.startswith('create_')]
    for method in create_methods[:10]:  # 只显示前10个
        print(f"  - {method}")
    
    if len(create_methods) > 10:
        print(f"  ... 还有 {len(create_methods) - 10} 个方法")
    
    print("\n测试完成!")

except Exception as e:
    print(f"❌ 测试出错: {str(e)}")
    import traceback
    traceback.print_exc()
