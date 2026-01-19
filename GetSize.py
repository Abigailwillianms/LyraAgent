from airtest.core.api import *
from GetWindowTitle import get_window_titles
from PIL import Image  # 需要安装Pillow库: pip install pillow

get_window_titles()

Window = input("请选择输入一个窗口标题：")
while not Window:
    Window = input("未找到窗口，请重新输入一个窗口标题：")

#并且告诉我你的思考过程，以及调用了几次工具，每次传入的参数
step=0
connect_device(f"Windows:///?title_re={Window}*")
# 1. 捕获截图
sleep(2)
snapshot(f"./images/images{step}.jpg")

# 2. 使用PIL打开图片并获取分辨率
img = Image.open(f"./images/images{step}.jpg")
width, height = img.size  # size属性返回(width, height)元组

print(f"截图分辨率: {width}x{height}")