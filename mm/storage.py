import shutil

def get_disk_usage(mountpoint):
    """Get disk usage with shutil.disk_usage

    Returns None tuple if the mountpoint does not exist or an unexpected exception is encountered.
    """
    try:
        usage_info = shutil.disk_usage(mountpoint) # disk disk usage in Bytes
    except Exception:
        usage_info = (None, None, None)
    keys = ("tot", "used", "free")
    return {k:usage_info[id] for id,k in enumerate(keys) }

