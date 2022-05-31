import datetime as dt

class FriendRequest:
    _id_1 = None
    _user1 = None
    _id_2 = None
    _user2 = None
    _sended = None
    _state_1 = None
    _state_2 = None

    def __init__(self,user1,user2,id1,id2,sended=dt.datetime.today(),state_1='Accepted',state_2='Pending'):
        self._id_1 = id1
        self._user1 = user1
        self._id_2 = id2
        self._user2 = user2
        self._sended = sended
        self._state_1 = state_1
        self._state_2 = state_2

    def set_state_2(self,state_2):
        self._state_2 = state_2

    def get_user_1(self):
        return self._user1
    def get_user_2(self):
        return self._user2
    def get_sended(self):
        return self._sended
    def get_state_2(self):
        return self._state_2

    def accept(self):
        self._state_2 = 'Accepted'
    def reject(self):
        self._state_1 = 'Rejected'
        self._state_2 = 'Rejected'

    def toString(self):
        return 'From : ' + self._user1 + '\nTo : ' + self._user2 + '\n ON : ' + self._sended.strftime("%m/%d/%Y, %H:%M:%S")

    def DictInfo(self):
        return {
        "id_1" : self._id_1,
        "id_2" : self._id_2,
        "receiver" : self._user2,
        "sender" : self._user1,
        "state_1" : self._state_1,
        "state_2" : self._state_2
        }
