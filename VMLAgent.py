from langchain.agents import create_agent
from VML.loadModel import VML
from airtest.core.api import *
from VMLTools.AirtestTools import AgentTouch,AgentKeyEvent
from VMLTools.RAGTools import GetRAG
from Memory.MemoryLoad import checkp,config, error_recorder
from Tools.GetWindowTitle import get_window_titles
from PIL import Image
import os
import glob

# 清空images文件夹下的图片文件
def clear_images_folder():
    # 确保images文件夹存在
    if not os.path.exists('./images'):
        os.makedirs('./images')
        print("已创建images文件夹")
        return
    
    # 获取所有图片文件
    image_files = glob.glob('./images/*.jpg')
    image_files.extend(glob.glob('./images/*.png'))
    image_files.extend(glob.glob('./images/*.jpeg'))
    
    # 删除所有图片文件
    for file in image_files:
        try:
            os.remove(file)
            print(f"已删除：{file}")
        except Exception as e:
            print(f"删除文件失败：{file} - {str(e)}")
    
    print(f"已清空images文件夹，共删除{len(image_files)}个文件")

# 清空images文件夹
clear_images_folder()

get_window_titles()

Window = input("请选择输入一个窗口标题：")
while not Window:
    Window = input("未找到窗口，请重新输入一个窗口标题：")

print("已找到窗口，请准备输入指令==========")



agent=create_agent(
    model=VML,
    tools=[AgentTouch,AgentKeyEvent,GetRAG],
    system_prompt="""你是一个强大的电脑使用者。
    对于工具调用，请记住以下几点：
    1.调用AgentTouch时传递的坐标是x,y两个float类型,而非列表或元组；
    2.请注意：如果你认为需要分多步操作，可以先规划当前页面的操作并退出，我后续会为你提供你打开的页面供你继续执行，请不要
    一直尝试同样的操作
    
    对于不同的窗口，请记住下面的一些操作流程：
    1.对于网易云音乐：播放音乐通过点击歌曲头像左侧的数字来播放
    2.对于qq音乐，播放音乐通过点击歌曲头像播放
    
    重要提示：
    - 我会提供之前的错误操作历史，请你分析并避免重复执行相同的错误操作
    - 如果你发现某个操作失败，请尝试不同的方法来完成任务
    - 每次操作前，请仔细观察当前界面状态，确保操作的准确性
    """,
    checkpointer=checkp,
)

#并且告诉我你的思考过程，以及调用了几次工具，每次传入的参数
step=0
# 连接设备 - 根据输入类型选择连接方式
if Window.isdigit():
    # 如果输入是数字，使用窗口句柄连接
    connect_device(f"Windows:///{Window}")
else:
    # 如果输入是字符串，使用标题正则连接
    connect_device(f"Windows:///?title_re={Window}*")
window = device().app.top_window()  # 获取当前窗口


while True:
    step=step+1
    Ins = input("请输入下一步指令：")
    window.set_focus()
    # 添加时间戳确保文件名唯一
    import time
    timestamp = int(time.time())
    initial_snapshot_file = f"./images/images{step}_{timestamp}.jpg"
    snapshot(initial_snapshot_file)
    img = Image.open(initial_snapshot_file)
    width, height = img.size
    # 获取当前步骤的错误历史
    error_history = error_recorder.get_error_history(step)
    
    # 构建错误历史提示
    error_prompt = ""
    if error_history:
        error_prompt = "\n\n错误历史：\n"
        for i, error in enumerate(error_history):
            error_prompt += f"{i+1}. 操作: {error['action']}\n   原因: {error['reason']}\n"
        error_prompt += "\n请避免重复执行上述错误操作，尝试不同的方法。"
    
    # 从阿里云RAG知识库检索相关错误信息
    rag_info = error_recorder.retrieve_error_from_rag(Ins)
    
    # 构建完整提示
    full_prompt = Ins
    if rag_info:
        full_prompt += "\n\n" + rag_info
    if error_prompt:
        full_prompt += error_prompt
    
    # 构建消息
    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"images/images{step}_{timestamp}.jpg"},
                {"text": full_prompt}]
        }]
    # 添加网络错误处理和重试机制
    max_retries = 1  # 最多重试1次
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            res = agent.invoke(
                {"messages": messages}
                , config
            )
            ret = res['messages'][-1].content
            print(ret)
            # 如果输出为Exit，直接跳出循环，等待用户输入下一条指令
            if ret == "Exit":
                break
            break  # 成功执行，跳出重试循环
        except Exception as e:
            # 检查是否为网络错误
            if "Failed to resolve" in str(e) or "ConnectionError" in str(type(e).__name__):
                retry_count += 1
                if retry_count <= max_retries:
                    print(f"网络暂时故障，正在第{retry_count}次重试...")
                    # 等待1秒后重试
                    import time
                    time.sleep(1)
                else:
                    print(f"网络错误，已达到最大重试次数：{e}")
                    # 记录错误并继续执行
                    error_recorder.record_error(
                        step=step,
                        action="网络请求",
                        reason=f"网络错误：{str(e)}"
                    )
                    # 打印错误步骤
                    print(f"【错误记录】步骤 {step}：网络请求 - 网络错误：{str(e)}")
                    # 构建默认响应
                    res = {"messages": [{"content": "网络暂时故障，请稍后重试"}]}
                    print("网络暂时故障，请稍后重试")
                    break
            else:
                # 其他错误，直接抛出
                raise
    # 如果ret已经是Exit，直接跳过评估循环
    if ret != "Exit":
        rew=0
        max_retries = 5  # 最大重试次数
        while ret!="Exit" and rew < max_retries:
            rew=rew+1
            print(f"正在评估下一步，当前第{rew}次尝试（最多{max_retries}次）")
            # 添加时间戳确保文件名唯一
            eval_timestamp = int(time.time())
            eval_snapshot_file = f"./images/images{step}_res{rew}_{eval_timestamp}.jpg"
            snapshot(eval_snapshot_file)
            img = Image.open(eval_snapshot_file)
            width, height = img.size
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": f"images/images{step}_res{rew}_{eval_timestamp}.jpg"},
                        {"text": "这是你完成的效果，请评估是否达成成果，若达成则严格输出且仅输出'Exit'(不要有其他任何内容)，若未达成则重试"}]
                }]
            # 添加网络错误处理和重试机制
            eval_max_retries = 1  # 最多重试1次
            eval_retry_count = 0
            
            while eval_retry_count <= eval_max_retries:
                try:
                    res = agent.invoke(
                        {"messages": messages}
                        , config
                    )
                    ret=res['messages'][-1].content
                    print(ret)
                    
                    # 记录错误步骤
                    if ret != "Exit":
                        # 提取模型的操作描述
                        action_description = ret
                        # 记录错误
                        error_recorder.record_error(
                            step=step,
                            action=action_description,
                            reason="操作未达成预期结果"
                        )
                        # 打印错误步骤
                        print(f"【错误记录】步骤 {step}：{action_description}")
                        print(f"已记录错误操作: {action_description}")
                    break  # 成功执行，跳出重试循环
                except Exception as e:
                    # 检查是否为网络错误
                    if "Failed to resolve" in str(e) or "ConnectionError" in str(type(e).__name__):
                        eval_retry_count += 1
                        if eval_retry_count <= eval_max_retries:
                            print(f"网络暂时故障，正在第{eval_retry_count}次重试...")
                            # 等待1秒后重试
                            import time
                            time.sleep(1)
                        else:
                            print(f"网络错误，已达到最大重试次数：{e}")
                            # 记录错误
                            error_recorder.record_error(
                                step=step,
                                action="网络请求",
                                reason=f"网络错误：{str(e)}"
                            )
                            # 打印错误步骤
                            print(f"【错误记录】步骤 {step}：网络请求 - 网络错误：{str(e)}")
                            # 构建默认响应
                            ret = "网络暂时故障，请稍后重试"
                            print(ret)
                            break
                    else:
                        # 其他错误，直接抛出
                        raise
        
        if rew >= max_retries and ret != "Exit":
            print(f"已达到最大评估次数{max_retries}，任务未完成")




