class User:
    #user info
    _id = None
    _username = None
    _email = None
    _lon = None
    _lat = None

    def __init__(self,id = None,username = "",email = "", lon = 0.00,lat = 0.00):
        self._id = id
        self._username = username
        self._email = email
        self._lon = lon
        self._lat = lat
    #user info
    def set_username(self,username):
        self._username = username
    def set_email(self,email = ""):
        self._email = email
    def set_lon(self,lon):
        self._lon = lon
    def set_lat(self,lat):
        self._lat = lat

    def get_id(self):
        return self._id
    def get_coords(self):
        return {
            "lat" : self._lat,
            "lon" : self._lon
        }
    def get_username(self):
        return self._username
    def get_email(self):
        return self._email

class RegularUser(User):
    _online = None
    _points = 0
    _pcoins = 0
    _num_of_friends = 0
    _at_event = False
    _finished_events = 0

    def __init__(self,id = None,username = "",email = "", lon = 0.00,lat = 0.00,points = 0,pcoins = 0,online = 0,num_of_friends=0,finished_events = 0):
        #user info
        super(User,self).__init__(id,username,email,lon,lat)
        self._online = online
        self._points = points
        self._pcoins = pcoins
        self._num_of_friends = num_of_friends
        self._finished_events = finished_events
    #
    #setter
    #
    def set_points(self, points):
        self._points=points
    def set_pcoins(self,pcoins):
        self._pcoins = pcoins
    def set_online(self,online):
        self._online = online
    def set_num_of_friends(self,nm):
        self._num_of_friends = nm
    def set_at_event(self,at_event = 1):
        if at_event == 1:
            self._at_event = True
        else:
            self._at_event = False

    def get_points(self):
        return self._points
    def get_pcoins(self):
        return self._pcoins
    def get_online(self):
        return self._online
    def get_online_string(self):
        if self._online == 0 :
            return 'Offline'
        else:
            return 'Online'
    def get_num_of_friends(self):
        return self._num_of_friends
    def get_at_event(self):
        if self._at_event:
            return "At Event"
        else:
            return "Not At Event"
    def finished_event(self):
        self._finished_events += 1
        if self._finished_events == 3:
            self._pcoins += 1
            self._finished_events = 0
        else:
            pass
    def point_sum(self,sum):
        self._points+=sum
    def pcoin_sum(self,p):
        self._pcoins += p

    def DictInfo(self):
        mdict = {
        "id" : self._id,
        "username": self._username,
        "email": self._email,
        "coords" : self.get_coords(),
        "points" : self._points,
        "online" : self._online
        }
        return mdict

    def StringInfo(self):
        return 'Username : ' + self._username + '\nFriends : ' + str(self._num_of_friends) + '\nState : ' + self.get_online_string() + '\n'+self.get_at_event()
