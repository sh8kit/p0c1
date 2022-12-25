import platform
from datashack.core.os import OS

def get_os()->OS:
    return OS.from_str(platform.system().lower())