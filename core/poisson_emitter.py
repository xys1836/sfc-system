import numpy as np
import sched, time
from threading import Timer

class PoissonEmitter():
    def __init__(self, lam):
        self.current_time = 0
        self.next_time = 0
        self.lam = lam
        self.is_output = False
        self.callback = None
        self.is_stop = True
        self.timer = None

    def start(self, func, *args):
        self.is_stop = False
        self.callback = func
        self.args = args
        self.reset_timer()

    def stop(self):
        self.is_stop = True
        self.timer.cancel()
        print "Generator is stopped"


    def output(self):
        self.is_output = True
        self.callback(self.args)
        if not self.is_stop:
            self.reset_timer()

    def reset_timer(self):
        self.is_output = False
        interval = np.random.poisson(self.lam)
        print "interval is: ", interval
        self.timer = Timer(interval, self.output, ())
        self.timer.start()

if __name__ == '__main__':

    sg = PoissonEmitter(5)
    def p(*args):
        print args[0]
    sg.start(p, 1, 2)
    time.sleep(20)
    sg.stop()