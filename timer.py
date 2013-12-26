from threading import Thread
from time import sleep

def newTimer(f, interval, *args):
        def nf(*args):
                while True:
                        f(*args)
                        sleep(interval)

        t = Thread(target=nf, args=args)
        t.start()
        return t

