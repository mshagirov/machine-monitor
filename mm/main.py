from monitor import MachineMonitor
from pprint import pp
from time import sleep

def main():
    m = MachineMonitor()
    
    pp(m.info)
    pp(m.metrics())
    for _ in range(10):
        print(m.metrics())
        sleep(5)


if __name__ == '__main__':
    main()
