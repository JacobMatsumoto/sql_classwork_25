import serial


"""
#START OF CO-PILOT
import os
import time

base = os.path.dirname(__file__)                # folder where the script lives
target = os.path.join(base, "write_here_pico.txt")

with open(target, "a", encoding="utf-8") as f:
    f.write(f"TEST {time.time()}\n")

print("Wrote to:", os.path.abspath(target))
#END OF CO-PILOT ADDING THIS TO WHAT I WAS SHOWN IN A VIDEO
"""

import os
import time

port = "Board CDC @ COM3"
baudrate = 115200
serial_connection = serial.Serial(port, baudrate)


base = os.path.dirname(__file__)                # folder where the script lives
target = os.path.join(base, "write_here_pico.txt")

while True:
    data = serial_connection.read(128)
    if data == "stop":
        break
    print(data)
    with open(target, "a", encoding="utf-8") as f:
        f.write(f"\n")





print("Wrote to:", os.path.abspath(target))

# destination_file.close()
# serial_connection.close()
