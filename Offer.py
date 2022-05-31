class Offer :
    _id = None
    _details = None
    _pcoins = None
    #constructor
    def __init__(self,id,details,pcoins):
        self._id = id
        self._details = details
        self._pcoins = pcoins
    #methods
    def DictInfo(self):
        return {
            "id": self._id,
            "details" : self._details,
            "pcoins" : self._pcoins
        }
    def toString(self):
        return "Details : " + self._details + " \nPcoins : " + str(self._pcoins)
    def set_details(self,details):
        self._details = details
    def get_pcoins(self):
        return self._pcoins
    def get_id(self):
        return self._id
