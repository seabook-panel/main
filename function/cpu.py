import psutil

def cpu_count_core():
    """
    物理CPU核心数
    """
    return psutil.cpu_count(logical=False)

def cpu_count_logical():
    """
    逻辑CPU核心数
    """
    return psutil.cpu_count()

def cpu_freq():
    """
    最大频率
    """
    return psutil.cpu_freq().max

def cpu_percent():
    """
    使用百分比
    """
    return psutil.cpu_percent(interval=0.5)