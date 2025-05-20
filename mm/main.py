from monitor import MachineMonitor
from pprint import pp
from time import sleep

def main():
    m = MachineMonitor()
    
    print('m.info:\n')
    pp(m.info)

    print('m:')
    print(m)
    print(m.__repr__())
    
    for _ in range(5):
        print(m.metrics())
        sleep(1)


if __name__ == '__main__':
    main()
