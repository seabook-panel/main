import psutil

def cpu_count_main():
    return psutil.cpu_count(logical=False)

def cpu_count_logical():
    return psutil.cpu_count()

def cpu_freq():
    return psutil.cpu_freq().max

def cpu_percent():
    return psutil.cpu_percent(interval=0.5)