from langchain_core.tools import tool
from airtest.core.api import *
from PIL import Image


@tool("点击", description="""此工具用于实现点击操作
    参数：
    x；点击点的横坐标
    y:点击点的纵坐标
    duration:长按的持续时间
    right_click:是否右键点击（Windows系统下适用）
    times:点击次数
    """)
def AgentTouch(x: float, y: float, times=1, **kwargs) -> str:
    try:
        # 动态查找最新截图
        import os, glob
        screenshot_files = glob.glob("./images/*.jpg")
        screenshot_files.sort(key=os.path.getmtime, reverse=True)
        if not screenshot_files:
            return "未找到截图文件"
        latest_file = screenshot_files[0]
        img = Image.open(latest_file)
        width, height = img.size
        x_air = width / 1000 * x
        y_air = height / 1000 * y
        touch(v=(x_air, y_air), times=times, **kwargs)
        return f"已成功点击{x},{y}"
    except Exception as e:
        return f"点击操作失败：{str(e)}"


@tool("键盘输入", description="""
    此工具用于键盘输入事件，
    参数：
    1.keyName:按键名称或输入的字符串
    2.**kwargs – 平台相关的参数

    按键名称对应如下：（注意引号中的{}是输入的格式，在进行按键输入时必须保留）
    {"ENTER": "{ENTER}",
    "RETURN": "{RETURN}",
    "ESC": "{ESC}",
    "TAB": "{TAB}",
    "BACKSPACE": "{BACKSPACE}",
    "DELETE": "{DEL}",
    "DEL": "{DEL}",
    "INSERT": "{INSERT}",
    "HOME": "{HOME}",
    "END": "{END}",
    "PAGE_UP": "{PGUP}",
    "PGUP": "{PGUP}",
    "PAGE_DOWN": "{PGDN}",
    "PGDN": "{PGDN}",
    "SPACE": " ",
    "WIN": "{LWIN}",
    "LWIN": "{LWIN}",
    "RWIN": "{RWIN}",
    "UP": "{UP}",
    "DOWN": "{DOWN}",
    "LEFT": "{LEFT}",
    "RIGHT": "{RIGHT}",
    "W": "w",
    "A": "a",
    "S": "s",
    "D": "d",
    "SHIFT": "+",
    "CTRL": "^",
    "ALT": "%",}
    """)
def AgentKeyEvent(keyname, **kwargs) -> str:
    try:
        # 特殊按键映射
        key_mappings = {
            "WIN": "{LWIN}",
            "LWIN": "{LWIN}",
            "RWIN": "{RWIN}",
            "CTRL": "^",
            "LCTRL": "^",
            "RCTRL": "^",
            "ALT": "%",
            "LALT": "%",
            "RALT": "%",
            "SHIFT": "+",
            "LSHIFT": "+",
            "RSHIFT": "+",
            "ENTER": "{ENTER}",
            "RETURN": "{RETURN}",
            "ESC": "{ESC}",
            "TAB": "{TAB}",
            "BACKSPACE": "{BACKSPACE}",
            "DELETE": "{DEL}",
            "DEL": "{DEL}",
            "INSERT": "{INSERT}",
            "HOME": "{HOME}",
            "END": "{END}",
            "PAGE_UP": "{PGUP}",
            "PGUP": "{PGUP}",
            "PAGE_DOWN": "{PGDN}",
            "PGDN": "{PGDN}",
            "SPACE": " ",
            "UP": "{UP}",
            "DOWN": "{DOWN}",
            "LEFT": "{LEFT}",
            "RIGHT": "{RIGHT}",
            "W": "w",
            "A": "a",
            "S": "s",
            "D": "d",
        }
        
        # 检查并转换特殊按键
        if keyname in key_mappings:
            keyname = key_mappings[keyname]
        
        keyevent(keyname, **kwargs)
        return "成功输入"
    except Exception as e:
        return f"键盘输入失败：{str(e)}"


@tool("键盘按下", description="""
    此工具用于按下键盘按键（不释放），适用于DirectInput移动操作
    参数：
    1.keyName:按键名称
    """)
def AgentKeyDown(keyname) -> str:
    try:
        # 特殊按键映射
        key_mappings = {
            "WIN": "{LWIN}",
            "LWIN": "{LWIN}",
            "RWIN": "{RWIN}",
            "CTRL": "^",
            "LCTRL": "^",
            "RCTRL": "^",
            "ALT": "%",
            "LALT": "%",
            "RALT": "%",
            "SHIFT": "+",
            "LSHIFT": "+",
            "RSHIFT": "+",
            "UP": "{UP}",
            "DOWN": "{DOWN}",
            "LEFT": "{LEFT}",
            "RIGHT": "{RIGHT}",
            "W": "w",
            "A": "a",
            "S": "s",
            "D": "d",
        }
        
        # 检查并转换特殊按键
        if keyname in key_mappings:
            keyname = key_mappings[keyname]
        
        # 按下按键
        keyevent(keyname, down=True)
        return f"已成功按下按键：{keyname}"
    except Exception as e:
        return f"键盘按下失败：{str(e)}"


@tool("键盘释放", description="""
    此工具用于释放键盘按键，适用于DirectInput移动操作
    参数：
    1.keyName:按键名称
    """)
def AgentKeyUp(keyname) -> str:
    try:
        # 特殊按键映射
        key_mappings = {
            "WIN": "{LWIN}",
            "LWIN": "{LWIN}",
            "RWIN": "{RWIN}",
            "CTRL": "^",
            "LCTRL": "^",
            "RCTRL": "^",
            "ALT": "%",
            "LALT": "%",
            "RALT": "%",
            "SHIFT": "+",
            "LSHIFT": "+",
            "RSHIFT": "+",
            "UP": "{UP}",
            "DOWN": "{DOWN}",
            "LEFT": "{LEFT}",
            "RIGHT": "{RIGHT}",
            "W": "w",
            "A": "a",
            "S": "s",
            "D": "d",
        }
        
        # 检查并转换特殊按键
        if keyname in key_mappings:
            keyname = key_mappings[keyname]
        
        # 释放按键
        keyevent(keyname, down=False)
        return f"已成功释放按键：{keyname}"
    except Exception as e:
        return f"键盘释放失败：{str(e)}"


@tool("鼠标移动", description="""
    此工具用于鼠标移动操作，适用于DirectInput控制
    参数：
    1.x:目标横坐标（0-1000）
    2.y:目标纵坐标（0-1000）
    3.duration:移动持续时间（秒）
    """)
def AgentMouseMove(x: float, y: float, duration=0.1) -> str:
    try:
        # 动态查找最新截图
        import os, glob
        screenshot_files = glob.glob("./images/*.jpg")
        screenshot_files.sort(key=os.path.getmtime, reverse=True)
        if not screenshot_files:
            return "未找到截图文件"
        latest_file = screenshot_files[0]
        img = Image.open(latest_file)
        width, height = img.size
        x_air = width / 1000 * x
        y_air = height / 1000 * y
        
        # 使用airtest的鼠标移动功能
        mouse_move(v=(x_air, y_air), duration=duration)
        return f"已成功移动鼠标到{x},{y}"
    except Exception as e:
        return f"鼠标移动失败：{str(e)}"


@tool("组合按键", description="""
    此工具用于执行组合按键操作，如Ctrl+C、Alt+Tab等
    参数：
    1.keys:按键组合列表，如["CTRL", "C"]
    """)
def AgentKeyCombo(keys: list) -> str:
    try:
        # 特殊按键映射
        key_mappings = {
            "WIN": "{LWIN}",
            "LWIN": "{LWIN}",
            "RWIN": "{RWIN}",
            "CTRL": "^",
            "LCTRL": "^",
            "RCTRL": "^",
            "ALT": "%",
            "LALT": "%",
            "RALT": "%",
            "SHIFT": "+",
            "LSHIFT": "+",
            "RSHIFT": "+",
        }
        
        # 构建组合按键字符串
        combo = ""
        for key in keys:
            if key in key_mappings:
                combo += key_mappings[key]
            else:
                combo += key
        
        # 执行组合按键
        keyevent(combo)
        return f"已成功执行组合按键：{'+'.join(keys)}"
    except Exception as e:
        return f"组合按键失败：{str(e)}"
