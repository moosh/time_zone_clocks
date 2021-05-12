# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import time
import board
import busio
import math
import displayio
from adafruit_st7789 import ST7789
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle


class Point:
    def __init__(self, in_x: int, in_y: int):
        self.x = in_x
        self.y = in_y
        self.cos_cache = {}  # (angle, cos)
        self.sin_cache = {}  # (angle, sin)

    def rotate(self, in_angle:float, in_rot_center: "Point"):
        s = math.sin(math.radians(in_angle))
        c = math.cos(math.radians(in_angle))
        self.x -= in_rot_center.x
        self.y -= in_rot_center.y
        x_new = self.x * c - self.y * s
        y_new = self.x * s + self.y * c
        self.x = int(x_new + in_rot_center.x)
        self.y = int(y_new + in_rot_center.y)


def create_display():
    # Release any resources currently in use for the displays
    displayio.release_displays()

    spi = busio.SPI(board.D12, board.D11)
    tft_cs = board.D9
    tft_dc = board.D10
    tft_rst = board.D6
    display_bus = displayio.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst
    )
    out_display = ST7789(display_bus, width=240, height=240, rowstart=80)
    return out_display


def clock_hand(in_origin: Point, in_base: int, in_len: int, in_time_offset: float, in_color:int) -> Triangle:
    # build the second hand pointing upward (90 degrees) then rotate to point
    # toward the current second (negative angles)
    half_base = int(in_base/2)
    a = Point(in_origin.x - half_base, in_origin.y)
    b = Point(in_origin.x + half_base, in_origin.y)
    c = Point(in_origin.x, in_origin.y - in_len)
    angle = 360.0 * in_time_offset / 60.0
    a.rotate(angle, in_origin)
    b.rotate(angle, in_origin)
    c.rotate(angle, in_origin)
    out_tri = Triangle(a.x, a.y, b.x, b.y, c.x, c.y, fill=in_color, outline=in_color)
    print (out_tri)
    return out_tri


display = create_display()

# Make the display context
surface = displayio.Group(max_size=16)
display.show(surface)

FACE_RADIUS = int(240/4)
FACE_COLOR = 0x202020
SECOND_HAND_BASE = 3
SECOND_HAND_LEN = int(240/4)
SECOND_HAND_COLOR = 0xFF0000
MINUTE_HAND_BASE = 5
MINUTE_HAND_LEN = int(240/6)
MINUTE_HAND_COLOR = 0xFFFFFF
HOUR_HAND_BASE = 5
HOUR_HAND_LEN = int(240/8)
HOUR_HAND_COLOR = 0xFFFFFF

prev_minute_i = 0
prev_hour_i = 0

prev_minute_hand1 = None
prev_minute_hand2 = None
prev_minute_hand3 = None
prev_minute_hand4 = None

prev_hour_hand1 = None
prev_hour_hand2 = None
prev_hour_hand3 = None
prev_hour_hand4 = None

second = 0.0
minute = 15.0
hour = 6.0 * 5
origin1 = Point(int(240/4), int(240/4))
origin2 = Point(int(240/4 + 240/2), int(240/4))
origin3 = Point(int(240/4), int(240/4 + 240/2))
origin4 = Point(int(240/4 + 240/2), int(240/4 + 240/2))
face1 = Circle(origin1.x, origin1.y, FACE_RADIUS, fill=FACE_COLOR, outline=FACE_COLOR)
face2 = Circle(origin2.x, origin2.y, FACE_RADIUS, fill=FACE_COLOR, outline=FACE_COLOR)
face3 = Circle(origin3.x, origin3.y, FACE_RADIUS, fill=FACE_COLOR, outline=FACE_COLOR)
face4 = Circle(origin4.x, origin4.y, FACE_RADIUS, fill=FACE_COLOR, outline=FACE_COLOR)

surface.append(face1)
surface.append(face2)
surface.append(face3)
surface.append(face4)
surface.append(clock_hand(origin1, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR))
surface.append(clock_hand(origin2, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR))
surface.append(clock_hand(origin3, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR))
surface.append(clock_hand(origin4, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR))
surface.append(clock_hand(origin1, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR))
surface.append(clock_hand(origin2, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR))
surface.append(clock_hand(origin3, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR))
surface.append(clock_hand(origin4, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR))
surface.append(clock_hand(origin1, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR))
surface.append(clock_hand(origin2, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR))
surface.append(clock_hand(origin3, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR))
surface.append(clock_hand(origin4, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR))

while True:
    time.sleep(1)
    second = (second + 1) % 60.0

    minute = (minute + 1/60) % 60.0
    hour = (hour + 1/360) % 60.0

    surface[4] = clock_hand(origin1, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR)
    surface[5] = clock_hand(origin2, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR)
    surface[6] = clock_hand(origin3, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR)
    surface[7] = clock_hand(origin4, HOUR_HAND_BASE, HOUR_HAND_LEN, hour, HOUR_HAND_COLOR)
    surface[8] = clock_hand(origin1, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR)
    surface[9] = clock_hand(origin2, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR)
    surface[10] = clock_hand(origin3, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR)
    surface[11] = clock_hand(origin4, MINUTE_HAND_BASE, MINUTE_HAND_LEN, minute, MINUTE_HAND_COLOR)
    surface[12] = clock_hand(origin1, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR)
    surface[13] = clock_hand(origin2, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR)
    surface[14] = clock_hand(origin3, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR)
    surface[15] = clock_hand(origin4, SECOND_HAND_BASE, SECOND_HAND_LEN, second, SECOND_HAND_COLOR)

