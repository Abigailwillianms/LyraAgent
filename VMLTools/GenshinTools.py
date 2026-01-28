from airtest.core.win.win import *
from langchain_core.tools import tool


@tool("角色移动", description="""
    此工具用于控制游戏角色移动，支持持续移动指定时间。
    参数：
    1. direction: 移动方向，可选值为：'W'(前), 'A'(左), 'S'(后), 'D'(右)
    2. duration: 移动持续时间（秒），默认为1秒

    示例：
    - 向前移动2秒: 游戏角色移动(direction='W', duration=2)
    - 向左移动1秒: 游戏角色移动(direction='A', duration=1)
    """)
def Genshin_move(direction: str, duration: float = 1.0) -> str:
    """
    控制游戏角色移动指定方向和持续时间

    Args:
        direction: 移动方向 (W/A/S/D)
        duration: 持续时间（秒）

    Returns:
        str: 操作结果描述
    """
    direction = direction.upper()
    valid_directions = ['W', 'A', 'S', 'D']
    if direction not in valid_directions:
        return f"方向参数无效，应为 {valid_directions} 之一"

    if duration <= 0:
        return "持续时间必须大于0"

    # 执行按键操作
    key_press(direction)
    time.sleep(duration)
    key_release(direction)

    return f"成功向{direction}方向移动{duration}秒"
