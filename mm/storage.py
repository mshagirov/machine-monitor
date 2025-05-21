import shutil

def get_disk_usage(mountpoint):
    """Get disk usage with shutil.disk_usage

    Returns None tuple if the mountpoint does not exist or an unexpected exception is encountered.
    """
    try:
        return shutil.disk_usage(mountpoint) # disk disk usage in Bytes
    except Exception:
        return None, None, None

