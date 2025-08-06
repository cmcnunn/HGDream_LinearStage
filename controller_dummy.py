import random 

def move_to(ser, x, y): 
    print(f"Moving to absolute position X: {x}, Y: {y}")
    return 

def move_home(ser):
    print("Homing stage")
    return

def rel_move_to(ser, dx, dy):
    print(f"Moving relatively by dX: {dx}, dY: {dy}")
    return

def zero_to(ser,midx,midy):
    print("Zeroing stage position")
    move_to(ser,midx,midy) #move to midpoints
    print("ZEROING COMPLETE...Stage should be at (0,0)")
    return

def find_range(ser): #dummy find range
    def get_distinct_pair(low, high):
        a = random.randint(low,round(high/2))
        b = random.randint(round((high/2)+1), high)
        if a != b:
            return a, b
        
    print("Finding range of motion")

    xmin, xmax = get_distinct_pair(0, 160)
    ymin, ymax = get_distinct_pair(0, 160)
    
    midpoint_int = lambda a, b: round((a + b) / 2)
    xmid = midpoint_int(xmax, xmin)
    ymid = midpoint_int(ymax, ymin)

    xtot_d = xmax - xmin
    ytot_d = ymax - ymin

    x_max = xtot_d/2
    x_min = -x_max

    y_max = ytot_d/2
    y_min = -y_max

    print(f"Range X:{x_min},{x_max} Y:{y_min},{y_max}")

    return xmin, xmax, ymin, ymax, xmid, ymid  # Dummy range values