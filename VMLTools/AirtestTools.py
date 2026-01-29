from langchain_core.tools import tool
from airtest.core.api import *
import ast
from PIL import Image


@tool("点击", description="""此工具用于实现点击操作。
    对于工具调用，请记住以下几点：
    参数：
    pos:元组，内部为两个坐标值，如（100,200）
    duration:长按的持续时间
    right_click:是否右键点击（Windows系统下适用）
    times:点击次数
    """)
def AgentTouch(pos, step: int = 1,  **kwargs) -> str:
    """
    修复AI可能传入错误格式的参数
    """
    # 处理pos参数：可能传入字符串或元组
    if isinstance(pos, str):
        try:
            # 尝试解析字符串格式的坐标
            if pos.startswith("[") and pos.endswith("]"):
                # 处理 "[293, 516]" 格式
                pos = ast.literal_eval(pos)
            elif "," in pos:
                # 处理 "293, 516" 格式
                pos = tuple(map(int, pos.split(",")))
        except:
            return f"无法解析坐标参数: {pos}"

    # 确保pos是元组或列表
    if isinstance(pos, (tuple, list)) and len(pos) >= 2:
        x, y = pos[0], pos[1]
    else:
        return f"坐标格式错误: {pos}"

    img = Image.open(f"./images/images11.jpg")
    width, height = img.size
    x_air = width / 1000 * x
    y_air = height / 1000 * y
    touch(v=(x_air, y_air), **kwargs)
    return f"已成功点击({x}, {y})"


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