from timing import now


def gen_timer(time_s):
    time_s *= 1000
    lastcheck = now()

    while True:
        if lastcheck + time_s < now():
            lastcheck += time_s
            yield True
        else:
            yield False
