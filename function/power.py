import platform
import subprocess
from enum import Enum

class PowerEvent(Enum):
    REBOOT = {
        'Windows': ['shutdown', '-r', '-t', '0'],
        'Linux': ['shutdown', '-h', 'now']
    }
    SHUTDOWN = {
        'Windows': ['shutdown', '-s', '-t', '0'],
        'Linux': ['shutdown', '-r', 'now']
    }

def power_control(event: PowerEvent):
    command = event.value.get(platform.system(), None)
    if command is None:
        return "<h1>海书面板提醒您：目前不支持该操作系统。</h1>唉？这是什么奇怪的系统，快去反馈给我们吧！识别ID：" + platform.system()

    subprocess.run(command)
