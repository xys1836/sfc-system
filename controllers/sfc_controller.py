from controllers.sfc_generator import SFCGenerator

class SFCController():
    def __init__(self):
        self.sfc_list = []
        self.sfc_id_dict = {}
        self.sfc_queue = None
        self.is_stop = True
        pass

    def add_sfc(self, sfc):
        self.sfc_id_dict[sfc.id] = sfc
        self.sfc_list.append(sfc)

    def remove_sfc(self, sfc_id):
        sfc = self.get_sfc_by_id(sfc_id)
        self.sfc_list.remove(sfc)
        del self.sfc_id_dict[sfc_id]
        pass

    def get_sfc_by_id(self, sfc_id):
        return self.sfc_id_dict.get(sfc_id, None)

    # def get_sfc_from_queue(self, sfc_queue):
    #     return sfc_queue.peek_sfc()  # this is blocking

    def run(self):
        while not self.is_stop:
            sfc = self.sfc_queue.peek_sfc()# this is blocking
            print "SFCController"
            print "get a new sfc", sfc.id
            self.add_sfc(sfc)


    def start(self, sfc_queue):
        self.is_stop = False
        self.sfc_queue = sfc_queue
        import thread
        thread.start_new_thread(self.run, ())


    def stop(self):
        self.is_stop = True


