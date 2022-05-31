import datetime as dt
import random as rd

class Code:
    _offer = None
    _codestring = None
    _when = None

    def __init__(self,offer,codestring = None,when = None):
        if codestring == None:
            self._offer = offer
            self.generate_code_string()
            self._when = dt.datetime.today()
        else:
            self._offer = offer
            self._codestring = codestring
            self._when = when

    def generate_code_string(self):
        self._codestring = ""
        for i in range(10):
            self._codestring += str(rd.randint(0,365)%10)
        self._codestring += str(self._offer.get_id())

    def DictInfo(self):
        return {
            "offer" : self._offer.DictInfo(),
            "code" : self._codestring,
            "whn" : self._when
        }
    def get_offer(self):
        return self._offer
    def get_codestring(self):
        return self._codestring
