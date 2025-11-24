# write_test.py
target = r"C:\Users\jacob\OneDrive\Desktop\sql_classwork_25\homework\sql_final_folder\write_here_pico.txt"

with open(target, "a", encoding="utf-8") as f:
    f.write("TEST WRITE\n")

print(target)
