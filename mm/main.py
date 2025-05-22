from monitor import MachineMetric
from time import sleep
from pprint import pp

def main():
    m = MachineMetric(config='mm/config.yaml')
    print(m)
    print(m.errors)
    print(m.storage_config)
    print(m.network_config)
    for _ in range(3):
        pp(m.metrics())
        sleep(1)


if __name__ == '__main__':
    main()
