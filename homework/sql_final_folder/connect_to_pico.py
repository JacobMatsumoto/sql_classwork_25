import serial
"""https://youtu.be/OfJ5Y1FlW94?si=VBlBWqDqlRUcVG3E -- Tons of help with this bit and the Thony file."""

port = "COM3"
baudrate = 115200
serial_connection = serial.Serial(port, baudrate)


target = open(r"c:\Users\jacob\OneDrive\Desktop\sql_classwork_25\homework\sql_final_folder\write_here_pico.txt", "ab") #Co-pilot only added the r here

while True:
    data = serial_connection.read(128) #reads 128 bytes
    line = data.decode("utf-8", errors="replace").rstrip("\r\n") #majority of this line is Co-pilot. I took what it gave me in another file and re-wrote part of it and repurposed it here.
    if "stop" in line:
        break

    print(line)
    if "Too close" in line:
        target.write(data)
        break





print(f"Wrote to:", {target})

target.close()
serial_connection.close()
