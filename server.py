import argparse
import enum
import sys
import time
from dataclasses import dataclass

try:
    import serial  # pyserial
except Exception as e:
    serial = None


class Level(enum.IntEnum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


@dataclass
class LogRecord:
    level: Level
    millis: int
    tag: str
    message: str


def percent_decode(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            try:
                out.append(chr(int(s[i+1:i+3], 16)))
                i += 3
                continue
            except Exception:
                pass
        out.append(s[i])
        i += 1
    return ''.join(out)


def parse_line(line: str) -> LogRecord | None:
    # Expect: L|level|millis|tag|message\n
    line = line.strip('\r\n')
    if not line or not line.startswith('L|'):
        return None
    parts = line.split('|', 4)
    if len(parts) != 5:
        return None
    _, lvl, ms, tag, msg = parts
    try:
        level = Level(int(lvl))
        millis = int(ms)
    except Exception:
        return None
    return LogRecord(level, millis, percent_decode(tag), percent_decode(msg))


def level_to_name(lvl: Level) -> str:
    return {
        Level.TRACE: 'TRACE',
        Level.DEBUG: 'DEBUG',
        Level.INFO: 'INFO',
        Level.WARN: 'WARN',
        Level.ERROR: 'ERROR',
    }.get(lvl, '?')


def format_record(rec: LogRecord, t0: float | None = None) -> str:
    ts = time.time()
    wall = time.strftime('%H:%M:%S', time.localtime(ts))
    rel = f"+{ts - t0:7.3f}s" if t0 else f"{rec.millis/1000:7.3f}s"
    tag = f"[{rec.tag}]" if rec.tag else ""
    return f"{wall} {rel} {level_to_name(rec.level):5} {tag} {rec.message}"


class BtLogClient:
    def __init__(self, port: str, baud: int = 9600, min_level: Level = Level.INFO):
        if serial is None:
            raise RuntimeError(
                'pyserial is not installed. Install with: pip install pyserial')
        self.port = port
        self.baud = baud
        self.min_level = min_level
        self._ser = None

    def open(self):
        self._ser = serial.Serial(self.port, self.baud, timeout=1)
        # Give the module a moment
        time.sleep(0.1)

    def close(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def run(self):
        if not self._ser:
            self.open()
        start = time.time()
        try:
            while True:
                raw = self._ser.readline().decode('utf-8', errors='replace')
                if not raw:
                    continue
                rec = parse_line(raw)
                if not rec or rec.level < self.min_level:
                    continue
                print(format_record(rec, t0=start))
        except KeyboardInterrupt:
            pass


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description='Bluetooth Log Client for HC-06 (SPP)')
    p.add_argument('-p', '--port', required=True, help='COM port (e.g., COM7)')
    p.add_argument('-b', '--baud', type=int, default=9600,
                   help='Baud rate of HC-06 UART (default 9600)')
    p.add_argument('-l', '--level', default='INFO', choices=[
                   'TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR'], help='Minimum level to display')
    args = p.parse_args(argv)

    try:
        lvl = Level[args.level]
    except KeyError:
        print('Invalid level', file=sys.stderr)
        return 2

    client = BtLogClient(args.port, args.baud, lvl)
    try:
        client.run()
    finally:
        client.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
