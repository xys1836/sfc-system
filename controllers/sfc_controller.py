from controllers.sfc_generator import SFCGenerator
class SFCController():
    def __init__(self):
        self.sfc_list = []
        self.sfc_id_dict = {}
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


