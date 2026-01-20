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
def AgentTouch(x: float, y: float, step: int, times=1, **kwargs) -> str:
    img = Image.open(f"./images/images{step}.jpg")
    width, height = img.size
    x_air = width / 1000 * x
    y_air = height / 1000 * y
    touch(v=(x_air, y_air), times=times, **kwargs)
    return f"已成功点击{x},{y}"


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
    "SPACE": " ",}
    """)
def AgentKeyEvent(keyname, **kwargs) -> str:
    keyevent(keyname, **kwargs)
    return "成功输入"