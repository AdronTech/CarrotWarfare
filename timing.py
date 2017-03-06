from time import time as time_s
from pygame.time import get_ticks as time_ms

now = time_ms
updates_per_sec = 30
update_delay = 1000/updates_per_sec
delta_time = update_delay
avg_redraw_rate = 0.0
avg_update_delay = 0.0


def protocol_update(log: bool):
    global avg_update_delay
    next_push = time_s()
    while True:
        count = 0
        while time_s() < next_push:
            yield
            count += 1
        next_push += 1
        avg_update_delay = (avg_update_delay + count) / 2
        if log:
            print(">update_rate: {:.2f}\tcount:{}\terror: {:.2f}".format(avg_update_delay, count, avg_update_delay - updates_per_sec))

update_counter = protocol_update(True)
update_counter.send(None)


def protocol_redraw(log: bool):
    global avg_redraw_rate
    next_push = time_s()
    while True:
        count = 0
        while time_s() < next_push:
            yield
            count += 1
        next_push += 1
        avg_redraw_rate = (avg_redraw_rate + count) / 2
        if log:
            print("]redraw_rate: {:.2f}\tcount:{}".format(avg_redraw_rate, count))

redraw_counter = protocol_redraw(True)
redraw_counter.send(None)
