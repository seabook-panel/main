import platform
import subprocess


def shutdown():
    if platform.system() == "Windows":
        subprocess.run(['shutdown', '-s', '-t', '0'])
    elif platform.system() == "Linux":
        subprocess.run(['shutdown', '-r', 'now'])
    else:
        return "<h1>海书面板提醒您：目前不支持该操作系统。</h1>唉？这是什么奇怪的系统，快去反馈给我们吧！识别ID：" + platform.system()