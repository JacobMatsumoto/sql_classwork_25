# print_paths.py
import os
import serial.tools.list_ports

# --- file path (write_here_pico.txt next to this script) ---
file_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "write_here_pico.txt"))

# --- device path (tries to pick the Pico/USB-CDC port) ---


def find_pico_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        if "pico" in desc or "board cdc" in desc or "usb serial" in desc:
            return p.device
    return ports[0].device if ports else ""


device_path = find_pico_port()

# Print exactly the two paths (one per line)
print(device_path)
print(file_path)
