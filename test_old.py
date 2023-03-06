import skywriter
import signal

max_x, max_y, max_z = 0, 0, 0
min_x, min_y, min_z = 65535, 65535, 65535

print('Skywriter is up and running')

@skywriter.move()
def move(x, y, z):
    print("Movement detected: x={}, y={}, z={}".format(x, y, z))

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
