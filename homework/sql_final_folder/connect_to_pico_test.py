# connect_to_pico_logger_filtered.py
"""Whole file is Co-pilot in order to connect specifically to the Pi and listen for something 
getting too close. It writes the data to the txt file."""
import os
import time
import serial
import serial.tools.list_ports


def find_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        if "pico" in desc or "board cdc" in desc or "usb serial" in desc:
            return p.device
    return ports[0].device if ports else None


port = find_port() or "COM3"      # change if needed
baudrate = 115200

base = os.path.dirname(__file__)
target = os.path.join(base, "write_here_pico.txt")

print("Using port:", port)
print("Logging to:", target)

try:
    ser = serial.Serial(port, baudrate, timeout=1)
except Exception as e:
    raise SystemExit(f"Failed to open serial port {port}: {e}")

with ser, open(target, "a", encoding="utf-8") as f:
    print("Connected. Waiting for data...")
    # ignore initial boot banner
    boot_deadline = time.time() + 2.0
    while time.time() < boot_deadline:
        _ = ser.readline()

    try:
        while True:
            raw = ser.readline()
            if not raw:
                continue
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            # only write if the line contains the exact substring "Too close"
            if "Too close" in line:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                out = f"{timestamp}  {line}\n"
                f.write(out)
                f.flush()      # ensure immediate disk write
                print("Logged:", out, end="")
            else:
                # optional: show other lines on console but don't log them
                print("Skipped:", line)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial closed.")
