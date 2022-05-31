#
#Event Class
#
class Event:
    #event info
    _id = 0
    _lon = 0.00
    _lat = 0.00
    _name = ""
    _points_g = 0
    _points_r = 0
    _cap = 0
    _prv = False
    _starts = dt.datetime.today()
    _ends = dt.datetime.today()
    #usr info
    _creator = None
    _participate = []

    def __init__(self,id = 0,name = "",lon = 0.00,lat = 0.00,points_g = 0,points_r = 0,cap = 0,prv = False,creator = None,participate = [],starts = dt.datetime.today(),ends = dt.datetime.today()):
        #event info
        self._id = id
        self._name = name
        self._lat = lat
        self._lon = lon
        self._points_g = points_g
        self._points_r = points_r
        self._cap = cap
        self._prv = prv
        self._starts = starts
        self._ends = ends
        #usr info
        self._creator = creator
        self._participate = participate

    #event info
    def set_name(self,name = ""):
        self._name = name
    def points(self,points_g = 0,points_r = 0):
        self.points_g = points_g
        self.points_r = points_r
    def set_cap(self,cap = 0):
        self._cap = cap
    def set_points_r(self,points_r):
        self._points_r = points_r
    def set_points_g(self,points_g):
        self._points_g = points_g
    #user info
    def set_creator(self,creator = None):
        self._creator = creator
    def set_usrs(self,participate = []):
        self._participate = participate
    #date info
    def set_starts(self,starts):
        self._starts = startsdef
    def set_ends(self,ends):
        self._ends = ends
    #
    #getter
    #
    #event info
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_points(self):
        return (self._points_g,self._points_r)
    def get_cap(self):
        return self._cap
    def get_points_r(self):
        return self._points_r
    def get_points_g(self):
        return self._points_g
    def get_prv(self):
        return self._prv
    def get_prv_string(self):
        if self._prv == 1:
            return "Private Event"
        else:
            return "Public Event"
    #date info
    def get_starts(self):
        return self._starts
    def get_ends(self):
        return self._ends
    #user info
    def get_creator(self):
        return self._creator
    def get_users(self):
        return self._participate
    def get_num_users(self):
        return len(self._participate)
    #
    #event string
    #
    def toString(self):
        return "Name : "+self._name + " Points Required : " +str(self._points_r)+" \nMax Capacity : "+str(self._cap)+" Number of People : "+str(len(self._participate))
    #
    #event string
    #
    #
    #event dict
    #
    def DictInfo(self):
        return {
        "id" : self._id,
        "name" : self._name ,
        "location" : self._location ,
        "points_gained" : self._points_g ,
        "points_required" : self._points_r ,
        "capacity" : self._cap ,
        "private" : self._prv,
        "starts" : str(self._starts ),#paizei na 8elei moda
        "ends" : str(self._ends) ,
        #usr info
        "creator" : self._creator ,
        "participate" : self._participate, #sigoura 8elei moda
        "participators_num" : self.get_num_users()
        }

    def add_usr(self,usr):
        self._participate.append(usr)
    def user_to_participate(self,usr):# an epistrepsei True mporei na mpei alliws oxi
        if self._cap == len(self._participate):
            return False
        for i in self._participate:
            if i.get_id() == usr.get_id():
                return False
        #den einai mesa kai capacity < max
        return True
