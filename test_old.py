#!/usr/bin/env python

import signal

import skywriter


some_value = 5000

print('Skywriter is up and running')

@skywriter.move()
def move(x, y, z):
    print( x, y, z )
    print("Skywriter moved")

@skywriter.flick()
def flick(start,finish):
    print('Got a flick!', start, finish)
    print("Skywriter flicked")

@skywriter.airwheel()
def spinny(delta):
    global some_value
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    print('Airwheel:', some_value/100)
    print("Skywriter airwheeled")

@skywriter.double_tap()
def doubletap(position):
    print('Double tap!', position)
    print("Skywriter double-tapped")

@skywriter.tap()
def tap(position):
    print('Tap!', position)
    print("Skywriter tapped")

@skywriter.touch()
def touch(position):
    print('Touch!', position)
    print("Skywriter touched")

print("Waiting for input...")
signal.pause()
