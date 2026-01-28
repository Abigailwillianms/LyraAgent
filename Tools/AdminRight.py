import sys
import ctypes
import os

def is_admin():
    """检查当前是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def adminSr():
    if not is_admin():
        # 如果不是管理员，则请求管理员权限重新运行当前脚本
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()  # 结束当前的非管理员进程

