


bit_dia = 6.35
contour_margin = 0.4

first_depth = 1.
rough_depth = 1.5
contour_depth = 2.

g_code = ""
line_number = 1

depth = 13.
diameter = 23.
x_center = 10.
y_center = 70.

cut_speed = 300
lead_in_speed = 200
plunge_speed = 75

contour_rad = round((diameter - bit_dia) / 2, 3)
rough_rad = round(contour_rad - contour_margin, 3)


def add_cmd(cmd: str):
    global g_code, line_number
    g_code += f"\nN{line_number} {cmd}"
    line_number += 1

def rough_circle():
    global x, y
    add_cmd(f"G03 X{round(x,3)} Z{z} I-{rough_rad} J0 F{cut_speed}")

def contour_circle():
    global x, y
    #x = x_center + contour_rad
    #add_cmd(f"G01 Z{z} F{plunge_speed}")
    #add_cmd(f"G01 X{round(x,3)} F{lead_in_speed}")
    add_cmd(f"G03 X{round(x,3)} Z{z} I-{contour_rad} J0 F{cut_speed}")
    #x -= 1
    #add_cmd(f"G00 X{x}")



add_cmd("G90")
z = 15.
add_cmd(f"G00 Z{z}")
x = x_center
y = y_center
add_cmd(f"G00 X{x} Y{y}")
z = 1.
add_cmd(f"G00 Z{z}")
z = 0.
x += rough_rad
add_cmd(f"G01 X{x} F{cut_speed}")
rough_circle()
z -= first_depth
rough_circle()
while z > -depth:
    z -= rough_depth
    if z < -depth:
        z = -depth
    rough_circle()
rough_circle()

z = 1.
add_cmd(f"G00 Z{z}")
x = x_center + contour_rad
add_cmd(f"G01 X{x} F{cut_speed}")
z = 0.
contour_circle()
z -= first_depth
contour_circle()
while z > -depth:
    z -= contour_depth
    if z < -depth:
        z = -depth
    contour_circle()
contour_circle()

z = 10.
add_cmd(f"G00 Z{z}")
print(g_code)



