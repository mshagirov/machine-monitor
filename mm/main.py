from monitor import MachineMetric
from time import sleep

def main():
    m = MachineMetric(config='mm/config.yaml')
    print(m)
    print(m.errors)
    print(m.storage_config)
    for _ in range(3):
        print(m.metrics())
        sleep(2.5)


if __name__ == '__main__':
    main()
