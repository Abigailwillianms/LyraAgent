from langchain_core.tools import tool
from airtest.core.api import *
from PIL import Image

"""def preTouch(x:int,y:int):
    x = 1.332 * x - 15.5
    y = 0.947 * y + 2.3"""

@tool("点击",description="""此工具用于实现点击操作
    参数：
    x；点击点的横坐标
    y:点击点的纵坐标
    duration:长按的持续时间
    right_click:是否右键点击（Windows系统下适用）
    times:点击次数
    """)
def AgentTouch(x: float,y: float,step:int , times=1, **kwargs) ->str:
    """此工具用于实现点击操作
    参数：
    x；点击点的横坐标
    y:点击点的纵坐标
    step:当前图像编号
    duration:长按的持续时间
    right_click:是否右键点击（Windows系统下适用）
    times:点击次数
    """
    img = Image.open(f"./images/images{step}.jpg")
    width, height = img.size
    x_air = width/1000 * x
    y_air = height/1000 * y
    touch(v=(x_air,y_air),times=times,**kwargs)
    snapshot(f"./images/images{step}.jpg")
    return f"已成功点击{x},{y}"

