import datetime as dt

class EventInvitation:
    _event = None
    _username_1 = None
    _id_1 = None
    _username_2 = None
    _id_2 = None
    _state_2 = 'Pending'
    _timestamp = None

    def __init__(self,event,username_1,username_2,id1,id2,timestamp=dt.datetime.today(),state_2 = 'Pending'):
        self._event = event
        self._username_1 = username_1#oanta o apostoleas
        self._id_1 = id1
        self._username_2 = username_2#panta o dekths
        self._id_2 = id2
        self._timestamp = timestamp
        self._state_2 = state_2

    def DictInfo(self):
        return {
            "event" : self._event.DictInfo(),
            "username_1" : self._username_1 ,
            "id_1" : self._id_1,
            "username_2" : self._username_2,
            "id_2" : self._id_2,
            "whn" : self._timestamp ,
            "state_2" : self._state_2
        }

    def get_event(self):
        return self._event
    def accept(self):
        self._state_2 = 'Accepted'
    def reject(self):
        self._state_2 = 'Rejected'
    def get_sender(self):
        return self._username_1
    def toString(self):
        return "From : " + self._username_1 +"\nWhen : " + str(self._timestamp )+ "\nEvent : " + self._event.get_name()
