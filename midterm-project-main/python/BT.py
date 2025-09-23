import logging
from time import sleep

from serial import Serial
from serial.serialutil import SerialException

log = logging.getLogger(__name__)

# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?


class Bluetooth:
    """
    The Bluetooth class is used to connect to the Arduino via Bluetooth.
    """

    def __init__(self):
        self.serial = Serial()

    def do_connect(self, port: str, baud: int = 9600) -> bool:
        self.serial.close()
        log.info(f"Connecting to {port}...")
        try:
            self.serial = Serial(port, baud, timeout=2)
            log.info("Success\n")
        except SerialException as e:
            log.warning(f"Fail to connect\n {e}")
            return False
        return True

    def disconnect(self):
        self.serial.close()

    def serial_write_string(self, data: str):
        send = data.encode("utf-8")
        self.serial.write(send)

    def serial_write_bytes(self, data: bytes):
        self.serial.write(data)

    def serial_read_string(self):
        waiting = self.serial.in_waiting
        if waiting >= 0:
            rv = self.serial.readline().decode("utf-8")[:-1]
            return rv
        return ""
