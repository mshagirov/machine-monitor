from monitor import MachineMetric
from time import sleep

def main():
    m = MachineMetric()
    print(m)
    for _ in range(3):
        print(m.metrics())
        sleep(5)


if __name__ == '__main__':
    main()
