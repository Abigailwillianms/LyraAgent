from LangTask import execute_agent_task
from Tools.GetWindowTitle import get_window_titles
from Tools.AdminRight import adminSr
adminSr()

get_window_titles()
step=0
while True:
    step=step+1
    WINDOW_TITLE = input("请输入窗口名：")
    INITIAL_INSTRUCTION = input("请输入接下来的指令：")
    # 执行任务
    result = execute_agent_task(WINDOW_TITLE, INITIAL_INSTRUCTION,nums=step)

#搜索并播放”原色“