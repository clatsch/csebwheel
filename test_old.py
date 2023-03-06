import skywriter
import signal

max_x, max_y, max_z = 0, 0, 0
min_x, min_y, min_z = 65535, 65535, 65535

@skywriter.move()
def move(x, y, z):
    global max_x, max_y, max_z, min_x, min_y, min_z

    if x < min_x:
        min_x = x
    if y < min_y:
        min_y = y
    if z < min_z:
        min_z = z
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y
    if z > max_z:
        max_z = z

    print(f"X: {x}, Y: {y}, Z: {z}, min_X: {min_x}, min_Y: {min_y}, min_Z: {min_z}, max_X: {max_x}, max_Y: {max_y}, max_Z: {max_z}")

@skywriter.airwheel()
def airwheel(delta):
    print(f"Airwheel: {delta}")

@skywriter.double_tap()
def doubletap(position):
    print(f"Double tap: {position}")

@skywriter.tap()
def tap(position):
    print(f"Tap: {position}")

@skywriter.touch()
def touch(position):
    print(f"Touch: {position}")

signal.pause()
