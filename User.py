
#
#User Class
#
class User:
    #user info
    _id = None
    _online = None
    _username = None
    _email = None
    _coords = None
    _points = 0
    _num_of_friends = 0
    _at_event = False
    #_my_friends = []#edw 8a periexontai ontothtes user
    def __init__(self,username = "",email = "", coords = "",points = 0,online = 0,my_friends = None,id = None,num_of_friends=0):
        #user info
        self._id = id
        self._username = username
        self._email = email
        self._coords = coords
        self._points = points
        self._online = online
        self._num_of_friends = num_of_friends
    #    self._my_friends = my_friends
    #
    #setter
    #
    #user info
    def set_username(self,username):
        self._username = username
    def set_email(self,email = ""):
        self._email = email
    def set_coords(self, coords):
        self._coords = coords
    def set_points(self, points):
        self._points=points
    def set_online(self,online):
        self._online = online
    def set_num_of_friends(self,nm):
        self._num_of_friends = nm
    def point_sum(self,sum):
        self._points+=sum
    def set_at_event(self,at_event = 1):
        if at_event == 1:
            self._at_event = True
        else:
            self._at_event = False
    #def set_friends(self,my_friends):
    #    self._my_friends=my_friends
    #
    #getter
    #
    #user info
    def get_id(self):
        return self._id
    def get_points(self):
        return self._points
    def get_username(self):
        return self._username
    def get_email(self):
        return self._email
    def get_coords(self):
        return self._coords
    def get_lat(self):
        return self._coords["lat"]
    def get_lon(self):
        return self._coords["lon"]
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
    #def get_friends(self):
    #    return self._my_friends
    #def get_many_friends(self):
    #    return len(self._my_friends)
    def user_dict(self):
        mdict = {
        "id" : self._id,
        "username": self._username,
        "email": self._email,
        "coords" : {
            "lat" : self._coords["lat"],
            "lon" : self._coords["lon"]
            },
        "points" : self._points,
        "online" : self._online
        }
        return mdict
    def StringInfo(self):
        return 'Username : ' + self._username + '\n Friends : ' + str(self._num_of_friends)
#
#Gia User
#
