#!/usr/bin/env python3
"""
测试CreateIndexRequest的参数结构
"""

import sys
print("测试CreateIndexRequest...")

try:
    from alibabacloud_bailian20231229 import models
    
    print("✅ 成功导入models模块")
    
    # 检查CreateIndexRequest类
    if hasattr(models, 'CreateIndexRequest'):
        print("✅ 找到CreateIndexRequest类")
        
        # 获取类的签名
        import inspect
        sig = inspect.signature(models.CreateIndexRequest.__init__)
        print("\nCreateIndexRequest构造函数参数:")
        print(sig)
        
        # 检查类的属性
        print("\nCreateIndexRequest类属性:")
        attrs = [attr for attr in dir(models.CreateIndexRequest) if not attr.startswith('_')]
        for attr in attrs[:20]:  # 只显示前20个
            print(f"  - {attr}")
        
        if len(attrs) > 20:
            print(f"  ... 还有 {len(attrs) - 20} 个属性")
        
        # 尝试创建一个实例
        print("\n尝试创建CreateIndexRequest实例...")
        try:
            request = models.CreateIndexRequest(
                name="测试知识库",
                description="测试描述"
            )
            print("✅ 成功创建CreateIndexRequest实例")
            print(f"  name: {request.name}")
            print(f"  description: {request.description}")
        except Exception as e:
            print(f"❌ 创建实例失败: {str(e)}")
    else:
        print("❌ 未找到CreateIndexRequest类")
        
    print("\n测试完成!")

except Exception as e:
    print(f"❌ 测试出错: {str(e)}")
    import traceback
    traceback.print_exc()
