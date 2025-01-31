"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-04-14 23:11:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import platform
import random
import time
from subprocess import DEVNULL, run

import cv2 as cv
import numpy as np

from .exceptions import StopExecution

ADBOREDER = ""
ADBPATH = ""
EXCURSIONX = [-10, 10]
EXCURSIONY = [-10, 10]
STOP = False


def connect(order="127.0.0.1:7555", path="resources\\lib\\adb"):
    """
    说明:
        连接ADB
    参数:
        :param order: ADB端口
    """
    global ADBOREDER, ADBPATH, STOP
    ADBOREDER = order
    ADBPATH = path
    STOP = False
    shell = [ADBPATH, "connect", ADBOREDER]
    result = run(shell, capture_output=True, check=False)
    status = "already connected" in str(result.stdout) or "connected to" in str(
        result.stdout
    )
    return status and stop


def stop():
    global STOP
    STOP = True


def kill():
    """
    说明:
        关闭ADB
    """
    global ADBOREDER, ADBPATH
    shell = [ADBPATH, "kill-server"]
    run(shell, stdout=DEVNULL, check=False)


def input_swipe(pos1=(919, 617), pos2=(919, 908), time: int = 100):
    """
    说明:
        滑动屏幕
    参数:
        :param pos1: 坐标1
        :param pos2: 坐标2
        :param time: 操作时间(毫秒)
    """
    global ADBOREDER, ADBPATH
    shell = [
        ADBPATH,
        "-s",
        ADBOREDER,
        "shell",
        "input",
        "swipe",
        str(pos1[0] + random.randint(*EXCURSIONX)),
        str(pos1[1] + random.randint(*EXCURSIONY)),
        str(pos2[0] + random.randint(*EXCURSIONX)),
        str(pos2[1] + random.randint(*EXCURSIONY)),
        str(int(time)),
    ]
    run(shell, check=False)


def input_tap(pos=(880, 362)):
    """
    说明:
        点击坐标
    参数:
        :param pos: 坐标
    """
    global ADBOREDER, ADBPATH
    shell = [
        ADBPATH,
        "-s",
        ADBOREDER,
        "shell",
        "input",
        "tap",
        str(pos[0] + random.randint(*EXCURSIONX)),
        str(pos[1] + random.randint(*EXCURSIONY)),
    ]
    run(shell, check=False)


def screenshot() -> cv.typing.MatLike:
    """
    截图
    """
    global ADBOREDER, ADBPATH, STOP
    if STOP:
        raise StopExecution()
    shell = [ADBPATH, "-s", ADBOREDER, "exec-out", "screencap", "-p"]
    result = run(shell, capture_output=True, check=False)

    # 将截图数据转换为 NumPy 数组
    image_array = np.frombuffer(result.stdout, np.uint8)

    screenshot = cv.imdecode(image_array, cv.IMREAD_COLOR)

    return screenshot
