import psutil


def memory_totol():
    mem = psutil.virtual_memory()
    zj = float(mem.total / 1024 / 1024 / 1024)
    memory_totol = '%.1f' % zj
    return memory_totol

def memory_used():
    mem = psutil.virtual_memory()
    ysy = float(mem.used / 1024 / 1024 / 1024)
    memory_used = '%.1f' % ysy
    return memory_used

def memory_free():
    mem = psutil.virtual_memory()
    kx = float(mem.free / 1024 / 1024 / 1024)
    memory_free = '%.1f' % kx
    return memory_free
    