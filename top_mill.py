


file_output = ""
line_number = 1

bit_dia = 0.75 * 25.4
overhang = round(0.30 * bit_dia, 2)

travel = round(bit_dia / 2, 2)
width = 210
x = width / 2
y = width / 2

tool_travel = 0

def add_cmd(cmd: str):
    global file_output, line_number
    file_output += f"N{line_number} {cmd}\n"
    line_number += 1


add_cmd("G21 G90 ;set metric / absolute")
add_cmd("G0 Z5")
add_cmd(f"G0 X{x} Y{y}")
add_cmd("G0 Z1")
add_cmd("G1 Z-0.2 F100")
add_cmd(f"G1 X{x} F400")

while travel < width - bit_dia:
    travel += overhang
    tool_travel += overhang
    x -= overhang
    tool_travel += overhang
    add_cmd(f"G1 X{round(x, 2)}")
    y += round(travel / 2, 2)
    tool_travel += round(travel / 2, 2)
    add_cmd(f"G1 Y{round(y, 2)}")
    x += travel
    tool_travel += travel
    add_cmd(f"G1 X{round(x, 2)}")
    y -= travel
    tool_travel += travel
    add_cmd(f"G1 Y{round(y, 2)}")
    x -= travel
    tool_travel += travel
    add_cmd(f"G1 X{round(x, 2)}")
    y += round(travel / 2, 2)
    add_cmd(f"G1 Y{round(y, 2)}")
    tool_travel += round(travel / 2, 2)
    travel += overhang

add_cmd("G0 Z5")
f = open(f"g_code\\top_mill.gcode", "w")
f.write(file_output)
f.close()

print(tool_travel, tool_travel/400)