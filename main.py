# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
"""
    G0 - Rapid Move
    G1 - Linear Move
    G2 - Circular Move (CW)
    G3 - Circular Move (CCW)
    G20 - Imperial
    G21 - Metric
    G90 - Absolute
    G91 - Incremental

    H - horizontal
    V - veritcal
    A - arc
    L
"""
import re
from os import write

tool_dia = 3.175
cut_depth = 0.5
feed_rate = 600
plunge_rate = 200
safe_height = 5

positioning = ""
file_output = ";"

x = 0
y = 0
z = 0


def add_cmd(cmd: str):
    global file_output
    file_output += f"\n{cmd}"


def move_to_path_start(start, pos_on_path):
    global x, y, z
    action = start[0:1]
    cmd_pos = start[1:].split(",")
    cmd_y = float(cmd_pos[1])
    if pos_on_path == "inside":
        cmd_y = cmd_y + tool_dia / 2
    elif pos_on_path == "outside":
        cmd_y = cmd_y + tool_dia / 2
    cmd = update_xyz(action, cmd_x=cmd_pos[0], cmd_y=cmd_y)
    add_cmd("; move to start of shape")
    add_cmd(f"G0 {update_xyz('M', cmd_z=safe_height)}")
    add_cmd(f"G0 {cmd}")
    add_cmd(f"G0 {update_xyz('M', cmd_z='0.5')}")


def update_xyz(action, cmd_x=None, cmd_y=None, cmd_z=None):
    global x, y, z
    absolute = re.match(r"[A-Z]", action) is not None
    cmd = ""
    if cmd_x is not None:
        x = float(cmd_x) if absolute else x + float(cmd_x)
        cmd = f"X{str(round(x, 4))}"
    if cmd_y is not None:
        y = float(cmd_y) if absolute else y + float(cmd_y)
        cmd += f" Y{str(round(y, 4))}"
    if cmd_z is not None:
        z = float(cmd_z) if absolute else z + float(cmd_z)
        cmd += f" Z{round(z, 4)}"
    cmd = cmd.lstrip(" ")
    return cmd


def path(obj: str, pos_on_path="center"):
    global positioning, x, y, z

    action = obj[0:1]
    if action.upper() == "A":
        # arc
        cmd = obj[1:].split(" ")
        radius = float(cmd[0])
        cmd_pos = cmd[1].split(",")
        cmd_x = float(cmd_pos[0])
        cmd_y = float(cmd_pos[1])
        d = tool_dia if cmd_x == 0 or cmd_y == 0 else tool_dia / 2
        if pos_on_path == "inside":
            if cmd_y == 0 or cmd_x + cmd_y == 0:
                if cmd_x + cmd_y == 0:
                    cmd_y = cmd_y - d if cmd_y > 0 else cmd_y + d
                cmd_x = cmd_x - d if cmd_x > 0 else cmd_x + d
            if cmd_x == 0 or cmd_x == cmd_y:
                if cmd_x == cmd_y:
                    cmd_x = cmd_x + d if cmd_x < 0 else cmd_x - d
                cmd_y = cmd_y + d if cmd_y < 0 else cmd_y - d
            radius -= tool_dia / 2
        elif pos_on_path == "outside":
            if cmd_y == 0 or cmd_x + cmd_y == 0:
                if cmd_x + cmd_y == 0:
                    cmd_y = cmd_y - d if cmd_y < 0 else cmd_y + d
                cmd_x = cmd_x - d if cmd_x < 0 else cmd_x + d
            if cmd_x == 0 or cmd_x == cmd_y:
                if cmd_x == cmd_y:
                    cmd_x = cmd_x + d if cmd_x > 0 else cmd_x - d
                cmd_y = cmd_y + d if cmd_y > 0 else cmd_y - d
            radius += tool_dia / 2
        cmd = update_xyz(action, cmd_x=cmd_x, cmd_y=cmd_y)

        add_cmd(f"G2 {cmd} R{str(round(radius, 4))} F{feed_rate}")
    elif action.upper() == "V":
        val = float(obj[1:].replace(' ', ''))
        cmd = update_xyz(action, cmd_y=val)
        add_cmd(f"G1 {cmd} F{feed_rate}")
    elif action.upper() == "H":
        val = float(obj[1:].replace(' ', ''))
        cmd = update_xyz(action, cmd_x=val)
        add_cmd(f"G1 {cmd} F{feed_rate}")
    elif action.upper() == "L":
        cmd = obj[1:].replace(' ', '')
        cmd_pos = cmd.split(",")
        cmd = update_xyz(action, cmd_x=cmd_pos[0], cmd_y=cmd_pos[1])
        add_cmd(f"G1 {cmd} F{feed_rate}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    name = "tension_plate"
    add_cmd(";BEGIN PROGRAM")
    add_cmd("G21 ;set metric\nG90 ;set absolute\n;")

    shapes = [
        {
            "name": "circle1",
            "posOnPath": "inside",
            "depth": -10,
            "start": "M21,19.75",
            "path": "a11.25 0,22.5a11.25 0,-22.5"
        },
        {
            "name": "circle2",
            "posOnPath": "inside",
            "depth": -10,
            "start": "M21,158.35",
            "path": "a11.25 0,22.5a11.25 0,-22.5"
        },
        {
            "name": "circle3",
            "posOnPath": "inside",
            "depth": -10,
            "start": "M12,78.1",
            "path": "a2.2 0,4.4a2.2 0,-4.4"
        },
        {
            "name": "perimeter",
            "posOnPath": "outside",
            "depth": -10,
            "start": "M10,5",
            "path": "a5 -5,5v170.6a5 5,5h22a5 5,-5v-170.6a5 -5,-5h-22"
        }
    ]
    """
    shapes = [
        {
            "name": "perimeter",
            "posOnPath": "outside",
            "depth": -0,
            "start": "M10,5",
            "path": "a5 -5,5v170.6a5 5,5h22a5 5,-5v-170.6a5 -5,-5h-22"
        }
    ]
    """

    for shape in shapes:
        add_cmd(f"; START {shape['name']}")
        p = shape["path"]

        pos = []
        for mat in re.finditer(r"[A-Za-z]", p):
            pos.append([mat.start(), mat.end()])

        print(pos)
        move_to_path_start(shape["start"], shape["posOnPath"])

        add_cmd("; begin cutting cycle")
        while z > shape["depth"]:
            z -= cut_depth
            if z <= shape["depth"]:
                z = shape["depth"]
            add_cmd(f"G1 Z{str(z)} F{plunge_rate}")
            for r in range(0, len(pos)):
                end = len(p) if r == len(pos) - 1 else pos[r + 1][0]
                path(p[pos[r][0]:end], shape["posOnPath"])
        add_cmd(f"G0 {update_xyz('M', cmd_z=safe_height)}")

        add_cmd(f"; END {shape['name']}\n;\n;")

    add_cmd(f"G0 {update_xyz('M', cmd_z=safe_height)}")
    c = update_xyz("M", cmd_x="0", cmd_y="0")
    add_cmd(f"G0 {c}")

    add_cmd(";END PROGRAM")
    f = open(f"g_code\\{name}.gcode", "w")
    f.write(file_output)
    f.close()
    #print(file_output)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
