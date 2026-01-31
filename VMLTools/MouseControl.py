import time
import ctypes
import random
from functools import wraps


def singleton(cls):
    """单例装饰器"""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class GameMouseController:
    def __init__(self):
        # Windows API常量
        self.MOUSEEVENTF_MOVE = 0x0001
        self.MOUSEEVENTF_ABSOLUTE = 0x8000

    def mouse_move_relative(self, dx, dy):
        """Windows原生相对鼠标移动"""
        ctypes.windll.user32.mouse_event(
            self.MOUSEEVENTF_MOVE,
            dx,
            dy,
            0, 0
        )

    def game_look(self, direction="right", duration=0.5, sensitivity=1.0):
        """
        游戏视角转动

        :param direction: "left" 或 "right"
        :param duration: 转动持续时间
        :param sensitivity: 鼠标灵敏度
        """
        # 根据方向确定符号
        sign = 1 if direction == "right" else -1

        # 基础移动速度（根据灵敏度调整）
        base_speed = int(40 * sensitivity)

        # 计算总帧数（60fps）
        frames = int(duration * 60)

        for i in range(frames):
            # 计算这一帧的移动距离（加入轻微变化）
            move_amount = sign * (base_speed + random.randint(-5, 5))

            # 执行相对移动
            self.mouse_move_relative(move_amount, 0)

            # 短暂等待
            time.sleep(1 / 60)


