import signal
import skywriter

@skywriter.flick()
def flick(start,finish):
    print('Got flick!', start, finish)

@skywriter.touch()
def touch(position):
    print('Got touch!', position)

@skywriter.airwheel()
def spinny(delta):
    print('Got a turn!', delta)

@skywriter.move()
def move(x, y, z):
    print('Got a move!', x, y, z)

signal.pause()

