from Queue import Queue
class SFCQueue(Queue):
    def __init__(self, max_size = 0):
        Queue.__init__(self, max_size)
        # self.sfc_queue = []
        # self.number_of_sfcs = 0

    def put_sfc(self, sfc):
        self.put(sfc)

    def peek_sfc(self):
        return self.get()




if __name__ == '__main__':
    q = SFCQueue()
    a = 1
    b = 2
    c = 3
    q.put_sfc(a)
    q.put_sfc(b)
    q.put_sfc(c)

    print q.peek_sfc()
    print q.peek_sfc()
    print q.peek_sfc()

    print q.empty()