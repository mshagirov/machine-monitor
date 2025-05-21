import platform
import psutil

from convert import byte2human

def machine_info():
    """Provides machine information as a dict of strings with following keys:
    
    - hostname : hostname of the machine on the network,
    - os : name of the operating system (OS),
    - version : OS version,
    - kernel : Linux kernel version (only on Linux),
    - arch : CPU architecture, e.g., x64, arm64, etc..
    - cpu : processor name,
    - cpu_count : number of physical CPU cores and logical in parentheses, e.g. "32 (64 logical)",
    - mem_tot : total physical memory (excludes swap).

    """
    ver = ''
    kernel = ''
    os_name = ''

    match platform.system():
        case 'Linux':
            try:
                os_ver_info = platform.freedesktop_os_release()
                os_name = os_ver_info.get('ID', 'Linux')
                ver = f"{os_ver_info.get('VERSION_ID', 'UNKNOWN')}"
                if 'VARIANT_ID' in os_ver_info:
                    ver = f"{ver} ({os_ver_info['VARIANT_ID']})"
            except OSError:
                os_name = "Linux"
                ver = 'Unknown'
            kernel = f'linux {platform.release()}'
        case 'Darwin':
            os_name = 'macos'
            ver = platform.mac_ver()[0]
            kernel = f"darwin {platform.release()}"
        case 'Windows':
            os_name = 'windows'
            ver = platform.release()
            kernel = platform.win32_ver()[1]

    return {'hostname' : platform.node(),
            'os' : os_name,
            'version' : ver,
            'kernel' : kernel,
            'arch' : platform.machine(),
            'cpu' : platform.processor(),
            'cpu_count' : f"{psutil.cpu_count(logical=False)} ({psutil.cpu_count()} logical)",
            'mem_tot' : byte2human(psutil.virtual_memory().total),
            }

