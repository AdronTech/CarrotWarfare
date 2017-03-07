import time


def gen_timer(time_s):
    time_s *= 1000
    lastcheck = time.time()

    while True:
        if lastcheck + time_s < time.time():
            lastcheck += time_s
            yield True
        else:
            yield False

