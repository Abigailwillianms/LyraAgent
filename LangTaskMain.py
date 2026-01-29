from LangTask import execute_agent_task
from Tools.GetWindowTitle import get_window_titles
from Tools.AdminRight import adminSr
from airtest.core.api import *
adminSr()

get_window_titles()
step=0

# 连接设备
# WINDOW_TITLE = input("请输入窗口名：")
WINDOW_TITLE = "原神"
try:
    connect_device(f"Windows:///?title_re={WINDOW_TITLE}*")
    window = device().app.top_window()  # 获取当前窗口
    window.set_focus()
except Exception as e:
    print(f"连接窗口失败")

while True:
    step=step+1

    INITIAL_INSTRUCTION = input("请输入接下来的指令：")
    # 执行任务
    result = execute_agent_task(window,INITIAL_INSTRUCTION,nums=step)

#搜索并播放”原色“