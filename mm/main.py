from monitor import MachineMetric
from time import sleep
from pprint import pp

def main():
    m = MachineMetric(config='mm/config.yaml')

    print(f"{' Information about the machine ':-^80}")
    pp(m.info)
    
    print(f"{' Machine metrics ':-^80}")
    for _ in range(1):
        pp(m.metrics())
        sleep(1)

    print(f"{' Configuration Information ':-^80}")

    print("Errors:")
    pp(m.errors)
    
    print("Storage config-s:")
    pp(m.storage_config)

    print("Network config-s:")
    pp(m.network_config)
    
    print("Connection config-s:")
    pp(m.connection_config)


if __name__ == '__main__':
    main()
