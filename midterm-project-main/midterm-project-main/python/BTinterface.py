import logging
from typing import Optional

from BT import Bluetooth

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


class BTInterface:
    def __init__(self, port: Optional[str] = None):
        log.info("Arduino Bluetooth Connect Program.")
        self.bt = Bluetooth()
        if port is None:
            ports_to_try = ["COM8", "COM9", "COM10"]
            port = None
            for try_port in ports_to_try:
                log.info(f"Trying to connect to {try_port}...")
                if self.bt.do_connect(try_port):
                    port = try_port
                    log.info(f"Successfully connected to {try_port}")
                    break
                    
            if port is None:
                log.error("Cannot auto-connect to any bluetooth port, using virtual mode")
                self.bt = None  # Virtual mode
        else:
            if not self.bt.do_connect(port):
                log.error(f"Cannot connect to {port}, using virtual mode")
                self.bt = None

    def start(self):
        # Auto start without waiting for input
        log.info("Auto starting, no need to press Enter")
        if self.bt:
            self.bt.serial_write_string("g")
        else:
            log.info("Virtual mode: simulating start signal")

    def get_UID(self):
        if self.bt:
            data = self.bt.serial_read_byte()
            if data and data != 0:
                log.debug(f"Bluetooth data received: {data}")
            return data
        return 0  # Virtual mode returns 0
        
    def get_ok(self):
        if self.bt:
            return self.bt.serial_read_string()
        return "ok"  # Virtual mode returns ok directly
        
    def send_action(self, dirc):
        # Send directly without waiting for response
        if self.bt:
            self.bt.serial_write_string(dirc)
            log.info(f"Sending command: {dirc}")
        else:
            log.info(f"Virtual mode: simulating command {dirc}")
        return

    def end_process(self):
        if self.bt:
            self.bt.serial_write_string("e")
            self.bt.disconnect()
        else:
            log.info("Virtual mode: simulating end process")


if __name__ == "__main__":
    test = BTInterface()
    test.start()
    test.end_process()
