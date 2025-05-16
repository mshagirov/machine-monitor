import shutil
import psutil

class Storage():
    def __init__(self):
       pass 
        

def get_disk_usage(mountpoint):
    try:
        return shutil.disk_usage(mountpoint) # disk disk usage in Bytes
    except FileNotFoundError:
        print(f"Error: {str(mountpoint)} is not a valid mount point, path doesn't exist")
        return None, None, None

partitions = psutil.disk_partitions()
# partitions : list of named tuples
mountpoints = [p.mountpoint for p in partitions]
# also might need : p=partitions[i] -> p.fstype and p.device

for p in partitions:
    tot, used, free = get_disk_usage(p.mountpoint) 
    # psutil.disk_usage ('/') -> user's used will be higher than actual usage
    if tot!=None:
        print(f"{p.device:<15} {p.mountpoint:<35} {p.fstype:^10}")
        print(f"tot:{tot/(1024**4):5.2f}TB; used:{used/(1024**3):5.2f}GB; free: {free/(1024**3):5.2f}GB ({100*used/tot:3.1f}% used)")
