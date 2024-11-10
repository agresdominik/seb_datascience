import time

from dht_22 import (
    readout_dht22
)

def main():
    
    while True:

        readout_dht22()

        time.sleep(5)


if __name__ == "__main__":
    main()