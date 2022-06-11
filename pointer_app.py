from User import User
from User import RegularUser
from FriendRequest import *
from Offer import *
from Code import *
from Event import *
from EventInvitation import *
#gia datetime
import datetime as dt
import calendar as clnd

#kivy things
from kivy.lang import Builder
from kivy.app import App

import re

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image

from kivy.properties import ListProperty, StringProperty

from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner

from kivy.uix.screenmanager import ScreenManager, Screen
#gia map
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy_garden.mapview import MapSource
#gia networking
import requests
import json
#gia functions
from functools import partial

#klash gia sundesh
class myConnection:
    url = 'http://localhost:8080'
    mdict = None
    def __init__(self,mdict,url_plus):
        self.mdict = mdict
        self.url = self.url+'/'+url_plus

    def send_dict(self):
        x = requests.post(self.url, data = json.dumps(self.mdict))
        return x
#klaseis me layouts koumpia kai o8ones
#to dropdown
class Control_Buttons(Spinner):
    pass
#to dropdown
class Create_Buttons(Spinner):
    pass
#kapoia koutia gia kaluterh emfanish
class MyBox(BoxLayout):
    pass
class MyBoxL(BoxLayout):
    pass

class ChoiceButton(Button):
    #krataei ena number
    _num = 0
    def __init__(self,num ,**kwargs):
        super(ChoiceButton, self).__init__(**kwargs)
        self._num = num
    def get_num(self):
        return self._num

class Chooser(TextInput):
    _for_location = False
    _current_user = None
    _profile_callback = None
    choicesfile = StringProperty()
    choiceslist = ListProperty([])

    def __init__(self, **kwargs):
        self.choicesfile = kwargs.pop('choicesfile', '')  # each line of file is one possible choice
        self.choiceslist = kwargs.pop('choiceslist', [])  # list of choices
        super(Chooser, self).__init__(**kwargs)
        self.multiline = False
        self.halign = 'left'
        self.bind(choicesfile=self.load_choices)
        self.bind(text=self.on_text)
        self.load_choices()
        self.dropdown = None

    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)
    #edw ta ypopshfia names
    def load_choices(self):
        if self.choicesfile:
            with open(self.choicesfile) as fd:
                for line in fd:
                    self.choiceslist.append(line.strip('\n'))
        self.values = []

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[0] == ord('\r'):  # enter selects current suggestion
            self.suggestion_text = ' '  # setting suggestion_text to '' screws everything
            self.text = self.values[0]
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
        else:
            super(Chooser, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def on_text(self, chooser, text):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
        if text == '':
            return
        #edw pairnw ypopshfia onomata
        else:
            #stelnw text
            mdict = {
                "name":str(self.text)
            }

            mc = myConnection(mdict,'simple_search')
            res = mc.send_dict()
            res = json.loads(res.text)
            values = []
            self.choiceslist = []#nomizw to eftiaksa...
            for r in res["info"]:
                u = from_Dict_to_User(r,self._current_user)
                if not(u == None):#an den einai o current user
                    self.choiceslist.append(u)
                    values.append(u.get_username())
            self.values = values
            if len(values) > 0:
                self.dropdown = DropDown()
                mc = 0
                for val in self.values:
                    self.dropdown.add_widget(ChoiceButton(num = mc,text=val, size_hint_y=None, height=48, on_release=self.do_choose))
                    mc+=1
                self.dropdown.open(self)

    def do_choose(self, butt):
        #vasika xrhsimopoiw mono names gia filling...polu mnhmh xwris logo?
        if self._for_location :
            #8a kanei fill h 8a phgainei se location profile?
            if self._profile_callback == None:
                #8a kanei fill
                self.text = self.choiceslist[butt.get_num()].get_name()#pairnw num apo koumpi
            else:
                self._profile_callback(self.choiceslist[butt.get_num()])
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
        else:
            #8a phgainei se user profile
            selected_user = self.choiceslist[butt.get_num()]#pairnw num apo koumpi
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            #ke edw kalw callback gia tade user
            self._profile_callback(user = selected_user)

    def set_current_user(self,usr):
        self._current_user = usr
    def set_profile_callback(self,callback):
        self._profile_callback = callback
    def set_if_location(self,i = True):
        self._for_location = i

class FriendsLayout(BoxLayout):
    _user = None
    _search_profile_callback = None
    def __init__(self,usr,tocallback_profile,to_invite = False,event = None,**kwargs):
        super(FriendsLayout, self).__init__(**kwargs)
        #pairnw friend request apo vash
        self._user = usr#apo auto 8a parw info gia friends
        mc = myConnection(self._user.DictInfo(), 'get_friends')
        res = mc.send_dict()
        res = json.loads(res.text)
        #ftiaxnw friend requests apo res

        fr = friends_creation(res)
        self.ids.search4friends.search_bar.set_current_user(self._user)
        #gia search pathma dropdown callback
        self.ids.search4friends.search_bar.set_profile_callback(tocallback_profile)#8a htan kalo na checkarw ke server?
        #self.ids.search4friends.subutton.bind(on_press = self.to_user_profile)
        for i in fr:
            f = Friends_Layout(i,tocallback_profile,to_invite,event)
            self.ids.main_content.friends.add_widget(f)
#to main content && ScrollView gia friends
#to main content gia Friends
class Friends_Layout(BoxLayout):
    _friend = None
    _to_user_profile = None
    _to_invite = None
    _event = None
    def __init__(self,friend,to_user_profile,to_invite = False,event = None,**kwargs):
        super(Friends_Layout, self).__init__(**kwargs)
        self._friend = friend
        self._to_user_profile = to_user_profile
        self._to_invite = to_invite
        self._event = event
        #ksereis oti prepei na to gemiseis
        self.ids.user_info.text = self._friend.StringInfo()
        if to_invite :
            self.ids.to_profile.text = 'Invite'
            #kalutera apla na stelnei inv
            self.ids.to_profile.bind(on_press = self.to_invite_profile)
        else:
            self.ids.to_profile.bind(on_press = self.to_user_profile)
        #8elw callback gia profile
    def to_user_profile(self,instance,**kwargs):
        self._to_user_profile(user = self._friend)
    def to_invite_profile(self,instance,**kwargs):
        self._to_user_profile(user = self._friend,ev = self._event)
#to main content gia Friends

#to main content gia FriendRequests
class FriendRequest_Layout(BoxLayout):
    _friendrequest = None
    _rm_callback = None
    def __init__(self,friendrequest,rm_callback,**kwargs):
        super(FriendRequest_Layout, self).__init__(**kwargs)
        self._rm_callback = rm_callback
        self._friendrequest = friendrequest
        #ksereis oti prepei na to gemiseis
        self.ids.user_info.text = self._friendrequest.StringInfo()
        #8elw callback gia accept h reject
        self.ids.accept.bind(on_press = self.accept_friend_request)
        self.ids.reject.bind(on_press = self.reject_friend_request)

    def accept_friend_request(self,instance,**kwargs):
        self._friendrequest.accepted()
        mc = myConnection(self._friendrequest.DictInfo(), 'accept_friend_request')
        res = mc.send_dict()
        #meta prepei na ginetai delete...
        self._rm_callback(self._friendrequest.get_id())
    def reject_friend_request(self,instance,**kwargs):
        self._friendrequest.rejected()
        mc = myConnection(self._friendrequest.DictInfo(), 'reject_friend_request')
        res = mc.send_dict()
        #meta prepei na ginetai delete...
        self._rm_callback(self._friendrequest.get_id())
#to main content gia FriendRequests
#to main content && ScrollView gia FriendRequests
class FriendsRequLayout(BoxLayout):
    _user = None
    _search_profile_callback = None
    _friendrequest_dict = {}
    def __init__(self,usr,tocallback_profile,**kwargs):
        super(FriendsRequLayout, self).__init__(**kwargs)
        #pairnw friend request apo vash
        self._user = usr#apo auto 8a parw info gia friend request
        mc = myConnection(self._user.DictInfo(), 'get_friend_request')
        res = mc.send_dict()
        res = json.loads(res.text)
        #ftiaxnw friend requests apo res
        fr = friend_request_creation(res)
        self.ids.search4friends.search_bar.set_current_user(self._user)
        #gia search pathma dropdown callback
        self.ids.search4friends.search_bar.set_profile_callback(tocallback_profile)#8a htan kalo na checkarw ke server?
        #self.ids.search4friends.subutton.bind(on_press = self.to_user_profile)
        if len(fr) == 0:
            self.ids.main_content.friend_requests.add_widget(Label(text = '\n\nIt\'s been quiet here...\nParticipate to Events to make new Friends !',font_size = '20px'))
        for i in range(0,len(fr)):
            f = FriendRequest_Layout(fr[i],rm_callback = self.remove_friend_request)
            self._friendrequest_dict[str(fr[i].get_id())] = i
            #f.bind(minimum_height = f.setter('height'))
            self.ids.main_content.friend_requests.add_widget(f)

    def remove_friend_request(self,anid):
        self.ids.main_content.friend_requests.remove_widget(self.ids.main_content.friend_requests.children[self._friendrequest_dict[str(anid)]])
#to main content && ScrollView gia FriendRequests

#gia na vgainoun diploi oi ari8moi sta spinners
def double_number_function(last):
    x = range(0,last)
    arr = []
    for k in x:
        if len(str(k)) > 1:
            arr.append(str(k))
        else:
            arr.append('0'+str(k))
    return arr

#pop up event
class myMarkerPopUp(MapMarkerPopup):
    _ev = None

    def __init__(self,some_text,to_layout, ev = None,**kwargs):
        super(myMarkerPopUp,self).__init__(**kwargs)
        to_layout.add_widget(Label(text = some_text,size = (100,50)))
        if isinstance(to_layout, MyBoxL):
            #edw mpainei koumpi gia location
            self._ev = ev
            b = Button(text="More Info",size_hint=(.85,.35),pos_hint={'center_x' : 0.5,'center_y':0.25})
            to_layout.add_widget(b)
        self.add_widget(to_layout)

#pop up event
#
#to profile tou xrhsth
#
class Profile_Layout(BoxLayout):
    _current_user = None
    _event = None
    _to_map = None
    def __init__(self,user,you,friend,to_map = None,to_invite = False,ev = None,**kwargs):
        super(Profile_Layout, self).__init__(**kwargs)
        #vazw ton user
        self._current_user = user
        self._to_map = to_map
        #gia username text input
        self.ids.info_layout.online.text = str(self.ids.info_layout.online.text) + self._current_user.get_online_string()
        self.ids.info_layout.username.text = str(self.ids.info_layout.username.text) + self._current_user.get_username()
        self.ids.info_layout.points.text = str(self.ids.info_layout.points.text) + str(self._current_user.get_points())
        self.ids.info_layout.friends.text = str(self.ids.info_layout.friends.text)
        self.ids.info_layout.coordinates.text = str(self.ids.info_layout.coordinates.text) + 'Latitude : ' + str(self._current_user.get_lat() ) + "\n"+' ' * 25+'Longitude : '+ str(self._current_user.get_lon())
        self.ids.info_layout.friends.text = str(self.ids.info_layout.friends.text)+ ' ' + str(self._current_user.get_num_of_friends())
        #gia on event
        self.ids.info_layout.at_event.text = self._current_user.get_at_event()

        #prepei na valw button gia add friend
        if you == None:
            pass
        else:
            #gia add friend
            b = Button(text='Add Friend', size_hint_y=0.07)
            b.bind(on_press = partial(self.send_friend_request, you ,self._current_user))
            self.add_widget(b)

            if friend==1 :
                b.disabled = True
            if to_invite:
                self._event = ev
                c = Button(text='Invite at Event', size_hint_y=0.07)
                c.bind(on_press = partial(self.send_event_invitation, you ,self._current_user))
                self.add_widget(c)
            else:
                self._event = ev
                c = Button(text='Invite at Event', size_hint_y=0.07)
                #c.bind(on_press = self.to_event_selection)
                self.add_widget(c)

    def send_friend_request(self,user1,user2,instance,**kwargs):#APO8HKEUONTAI TA DIPLA GTI EIMAI XAZOS
        mdict = {
            "msg" : {
                "username1":str(user1.get_username()),
                "id1" : str(user1.get_id()),
                "username2":str(user2.get_username()),
                "id2" : str(user2.get_id())
            }
        }
        mc = myConnection(mdict,'send_friend_request')
        res = mc.send_dict()
        res = json.loads(res.text)
        if res["info"] == '1':
            #8a paei next
            instance.disabled = True
        else:
            pass
            #8a exw message alert
    # 8a phgainei na vrei se poio event 8a ton proskalesei
    def send_event_invitation(self,user1,user2,instance,**kwargs):
        mdict = {
            "msg" : {
                "eid" : str(self._event.get_id()),
                "username1":str(user1.get_username()),
                "username2":str(user2.get_username())
            }
        }
        mc = myConnection(mdict,'send_event_invitation')
        res = mc.send_dict()
        res = json.loads(res.text)
        if res["info"] == '1':
            #8a paei to_map
            self._to_map(None)
        else:
            #exw message alert
            popup = Popup(title='Error',content=Label(text='You have already sent \nan invitation to this user !'),size_hint=(None, None), size=(235,135))
            popup.open()

class Event_Creation_Layout(BoxLayout):
    _to_map = None
    _user = None

    def __init__(self,user = None,to_map = None,**kwargs):
        super(Event_Creation_Layout, self).__init__(**kwargs)
        self._user = user
        self._to_map = to_map
        self.start_spinners()
        self.ids.info_layout.event_datetimes_1.ids.se_label.text = "Start"
        self.ids.info_layout.event_datetimes_2.ids.se_label.text = "End"
        self.ids.info_layout.subutton.bind(on_press = self.to_map)

    def to_map(self,instance,**kwargs):
        dt_value_1 = self.ids.info_layout.event_datetimes_1.ids.spinner_year.text+'/'+self.ids.info_layout.event_datetimes_1.ids.spinner_month.text+'/'+self.ids.info_layout.event_datetimes_1.ids.spinner_day.text+' '+self.ids.info_layout.event_datetimes_1.ids.spinner_hour.text+':'+self.ids.info_layout.event_datetimes_1.ids.spinner_minute.text
        dt_value_2 = self.ids.info_layout.event_datetimes_2.ids.spinner_year.text+'/'+self.ids.info_layout.event_datetimes_2.ids.spinner_month.text+'/'+self.ids.info_layout.event_datetimes_2.ids.spinner_day.text+' '+self.ids.info_layout.event_datetimes_2.ids.spinner_hour.text+':'+self.ids.info_layout.event_datetimes_2.ids.spinner_minute.text

        self._to_map(e = Event(name = str(self.ids.info_layout.name.text), points_g = int(self.ids.info_layout.points_earned.text),cap = int(self.ids.info_layout.capacity.text),creator = self._user,starts = dt.datetime.strptime(dt_value_1, '%Y/%B/%d %H:%M'),ends = dt.datetime.strptime(dt_value_2, '%Y/%B/%d %H:%M')))

    def start_spinners(self):
        #prepei na pairnoun times
        #gia spinners 1
        self.ids.info_layout.event_datetimes_1.ids.spinner_year.values = [str(dt.datetime.today().year) , str(dt.datetime.today().year + 1)]
        self.ids.info_layout.event_datetimes_1.ids.spinner_year.text = str(dt.datetime.today().year)

        self.ids.info_layout.event_datetimes_1.ids.spinner_month.values = list(clnd.month_name[1:])
        self.ids.info_layout.event_datetimes_1.ids.spinner_month.text = str(clnd.month_name[dt.datetime.today().month])

        x = double_number_function(30)
        self.ids.info_layout.event_datetimes_1.ids.spinner_day.values = x[1:]
        self.ids.info_layout.event_datetimes_1.ids.spinner_day.text = str(x[dt.datetime.today().day])
        del(x)

        self.ids.info_layout.event_datetimes_1.ids.spinner_hour.values = double_number_function(24)
        self.ids.info_layout.event_datetimes_1.ids.spinner_minute.values = double_number_function(60)

        #gia spinners 2
        self.ids.info_layout.event_datetimes_2.ids.spinner_year.values = [str(dt.datetime.today().year) , str(dt.datetime.today().year + 1)]
        self.ids.info_layout.event_datetimes_2.ids.spinner_year.text = str(dt.datetime.today().year)

        self.ids.info_layout.event_datetimes_2.ids.spinner_month.values = list(clnd.month_name[1:])
        self.ids.info_layout.event_datetimes_2.ids.spinner_month.text = str(clnd.month_name[dt.datetime.today().month])

        x = double_number_function(30)
        self.ids.info_layout.event_datetimes_2.ids.spinner_day.values = x[1:]
        self.ids.info_layout.event_datetimes_2.ids.spinner_day.text = str(x[dt.datetime.today().day])
        del(x)

        self.ids.info_layout.event_datetimes_2.ids.spinner_hour.values = double_number_function(24)
        self.ids.info_layout.event_datetimes_2.ids.spinner_minute.values = double_number_function(60)

    def check_restrictions(self):
        try:
            int(self.ids.info_layout.points_earned.text)
            int(self.ids.info_layout.capacity.text)
            #gia diarkeia ti kanw?
            #edw 8elw popup ke 8a to gurnaw se None, auto an den exoun mpei swsta ta datetimes
            if len(self.ids.info_layout.name.text) > 4:
                self.ids.info_layout.subutton.disabled = False
            elif self._creator.get_points() < int(self.ids.info_layout.points_earned.text):
                popup = Popup(title='Error',content=Label(text ='You don\'t have enough points.'),size_hint=(None, None), size=(275,125))
                popup.open()
            else:
                self.ids.info_layout.subutton.disabled = True
        except ValueError:
            self.ids.info_layout.subutton.disabled = True

    def check_date_restrictions(self,obj,**kwargs):
        #gia spinners
        dt_value_1 = self.ids.info_layout.event_datetimes_1.ids.spinner_year.text+'/'+self.ids.info_layout.event_datetimes_1.ids.spinner_month.text+'/'+self.ids.info_layout.event_datetimes_1.ids.spinner_day.text+' '+self.ids.info_layout.event_datetimes_1.ids.spinner_hour.text+':'+self.ids.info_layout.event_datetimes_1.ids.spinner_minute.text
        dt_value_2 = self.ids.info_layout.event_datetimes_2.ids.spinner_year.text+'/'+self.ids.info_layout.event_datetimes_2.ids.spinner_month.text+'/'+self.ids.info_layout.event_datetimes_2.ids.spinner_day.text+' '+self.ids.info_layout.event_datetimes_2.ids.spinner_hour.text+':'+self.ids.info_layout.event_datetimes_2.ids.spinner_minute.text
        try :

            if dt.datetime.strptime(dt_value_1, '%Y/%B/%d %H:%M') < dt.datetime.strptime(dt_value_2, '%Y/%B/%d %H:%M'):#8elw ke duration
                self.to_submit()
            else:
                popup = Popup(title='Error',content=Label(text ='The event duration is little.'),size_hint=(None, None), size=(275,125))
                popup.open()
        except ValueError:
            popup = Popup(title='Error',content=Label(text ='No values for starting or ending dates .'),size_hint=(None, None), size=(275,125))
            popup.open()

    def my_on_focus(self,instance,focus,**kwargs):
        if focus :
            pass
        else:
            self.check_restrictions()

    #8a paizei ena pop up pou 8a enhmerwnei gia to ti paizei me podous ke capacity
    def to_submit(self):
        if int(self.ids.info_layout.points_loose.text)/int(self.ids.info_layout.capacity.text) >= 100 and int(self.ids.info_layout.points_earned.text)/int(self.ids.info_layout.capacity.text) >= 500 :
            popup = Popup(title='Constraints are satisfied.',content=Label(text = 'Continue'),size_hint=(None, None), size=(275,125))
            popup.open()
        else:
            sub_layout = SubmitLayout()
            popup = Popup(title='Constraints are not satisfied.',content=sub_layout,size_hint=(None, None), size=(275,125),auto_dismiss=False)
            popup.content.ids.save.text = 'Modify'
            popup.content.ids.save.bind(on_press = self.modify_points)
            popup.content.ids.dismiss.bind(on_press = popup.dismiss)
            popup.open()

    def modify_points(self,instance,**kwargs):
        self.ids.info_layout.points_loose.text = str(int(self.ids.info_layout.capacity.text) * 100)
        self.ids.info_layout.points_earned.text = str(int(self.ids.info_layout.capacity.text) * 500)

#tosubmitLayout
class SubmitLayout(BoxLayout):
    pass
#ta spinner mou
class SpinnerLayout(GridLayout):
    pass
#to main screen
class Second_Screen(Screen):
    _user = None
    _temp_event = None

    def __init__(self,usr ,**kwargs):
        super(Second_Screen, self).__init__(**kwargs)
        self._user = usr
        print(str(self._user.DictInfo()))
        self._user.set_online(1)
        #prepei na kanw bind tis leitourgies twn koumpiwn
        self.ids.aka.info_layout.map_opp.options_layout.bind(text=self.spinner_selected_value)
        mmap = MapView(zoom=11, lat=self._user.get_lat(), lon=self._user.get_lon(),map_source=MapSource(min_zoom=3))
        #otan 8elw na ftiaksw event ,tote mporw na create events
        self.ids.aka.info_layout.map_opp.create_buttons.bind(text=self.to_create)
        #8elw na emfanizw me kedro to position mou
        #gia na paw se position                                                                                                                                 edw prepei na vazw alla pragmata...
        self.ids.aka.info_layout.map_opp.mpos.bind(on_press=lambda instance: self.manager.children[0].ids.aka.info_layout.children[0].sync_to(MapView(zoom=11, lat=self._user.get_lat(), lon=self._user.get_lon(),map_source=MapSource(min_zoom=3))))
        #vazw map
        self.ids.aka.info_layout.add_widget(mmap)
    #gia control Spinners
    def spinner_selected_value(self,instance, value,**kwargs):
        if self.ids.aka.info_layout.map_opp.options_layout.text == "Map":
            self.to_map(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Profile":
            self.to_profile(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Friends":
            self.to_friends(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Friend\nRequests":
            self.to_friend_requests(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Events":
            self.to_events(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Invite At Event":
            self.invitation_proc(None)
        elif self.ids.aka.info_layout.map_opp.options_layout.text == "Settings":
            self.to_settings(None)
        #to allo arxikopoieitai
        self.ids.aka.info_layout.map_opp.create_buttons.text = 'Create'
    #gia create spinners
    def to_create(self,instance, value,**kwargs):
        if self.ids.aka.info_layout.map_opp.create_buttons.text == "Create Event":
            self.create_event(None)
        #to allo arxikopoieitai
        self.ids.aka.info_layout.map_opp.options_layout.text = 'Control Buttons'

    #meta thn epituxh dhmiourgia location --> to map?
    def to_map_after_name(self,e):
        self.to_map(None)
        self._temp_event = e#auto 8a allaksei ?
        print(str(e.DictInfo()))
        #kanw disable ola
        #self.disable_all()
        #gia na ftiaksw locations
        self.ids.aka.info_layout.children[0].bind(on_touch_up=self.map_double_tap)
        #vazw ena submit button katw aristera
        b = Button(text = "Create",size_hint_x = .15 , size_hint_y = .05 ,pos_hint= {'x' : .095 , 'y' : .05})
        b.bind(on_press = self.save_event)
        self.ids.aka.add_widget(b)
        return self.manager

    def save_event(self,instance,**kwargs):
        #dhmiourgia Location , ta constraints ta tirhses prin
        #me ena pop_up , 8a ftiaksw ena submitLayout
        sub_layout = SubmitLayout()
        popup = Popup(title='Are you sure you want to create this Event ?',content=sub_layout,size_hint=(None, None), size=(275,125),auto_dismiss=False)
        popup.content.ids.save.bind(on_press = self.send_event)
        popup.content.ids.save.bind(on_release = popup.dismiss)
        popup.content.ids.dismiss.bind(on_press = popup.dismiss)
        popup.open()

    def send_event(self,instance , **kwargs):
        print(str(self._temp_event.DictInfo()))
        mc = myConnection(self._temp_event.DictInfo(), 'event_creation')
        res = mc.send_dict()
        self.ids.aka.remove_widget(self.ids.aka.children[0])
        self.to_map(None)
    #gia double tap se map
    def map_double_tap(self, instance,touch):
        if touch.is_double_tap:
            #pairnw suntetagmenes analoga me click
            a = self.ids.aka.info_layout.children[0].get_latlon_at(x=touch.pos[0],y=touch.pos[1])
            #allazw pragmata gia location
            self._temp_event.set_coord(lat = a.lat,lon = a.lon)
            #loipon, 8a mpei h kanonikh klash mazi me location
            mmarker = myMarkerPopUp(lon=a.lon,lat=a.lat,ev = self._temp_event,to_layout = MyBoxL(), some_text = self._temp_event.toString(),source="1mmarker.png")
            mmarker.bind(on_press = self.remove_lmarker)
            self.ids.aka.info_layout.children[0].add_marker(mmarker)
            #mia fora 8a ftiakseis Location
            self.ids.aka.info_layout.children[0].unbind(on_touch_down=self.map_double_tap)
            #8a vgalw pop up
            #xreiazomai xroniko delay gia ta double taps ?

    def remove_lmarker(self,instance , **kwargs):
        self.ids.aka.info_layout.children[0].remove_widget(instance)
        #gia na ftiaksw locations
        self.ids.aka.info_layout.children[0].bind(on_touch_down=self.map_double_tap)
    #gia na phgainw se map
    def to_map(self,instance,**kwargs):
        self.manager.current = 'second_light'
        self.manager.children[0].ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        mmap = MapView(zoom=11, lat=64.64, lon=37.37,map_source=MapSource(min_zoom=3))
        self.manager.children[0].ids.aka.info_layout.add_widget(mmap)
        return self.manager
    #paw se friend_requests
    def to_friend_requests(self,instance,**kwargs):
        self.manager.current = 'second_light'
        #vgazw to map
        self.ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        fr = FriendsRequLayout(usr = self._user,tocallback_profile = self.to_profile_with_u)
        self.ids.aka.info_layout.add_widget(fr)
        return self.manager
    #dhmiourgia event
    def create_event(self,instance,**kwargs):#den exw ftiaksei to antistoixo
        self.manager.current = 'second_light'
        #vgazw to map
        self.manager.children[0].ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        #vazw to profile
        p = Event_Creation_Layout(user = self._user,to_map = self.to_map_after_name)
        self.manager.children[0].ids.aka.info_layout.add_widget(p)

        return self.manager
    #to profile mu
    def to_profile(self,instance,**kwargs):
        self.manager.current = 'second_light'
        #vgazw to map
        self.ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        #vazw to profile
        p = Profile_Layout()
        self.ids.aka.info_layout.add_widget(p)

        return self.manager
    def to_friends(self,instance,**kwargs):
        self.manager.current = 'second_light'
        #vgazw to map
        self.ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        fr = FriendsLayout(usr = self._user,tocallback_profile = self.to_profile_with_u)
        self.ids.aka.info_layout.add_widget(fr)

        return self.manager

    #paw se profile mazi me user
    def to_profile_with_u(self,user,**kwargs):
        self.manager.current = 'second_light'
        #vgazw to map
        self.ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        #proetoimasia tou dict
        mdict = {"self" : self._user.DictInfo(), "user" : user.DictInfo()}
        #prepei na checkarw an o user einai filos h exw steilei friend_request
        print(str(mdict))
        mc = myConnection(mdict,'check_if_friend')
        res = mc.send_dict()
        res = json.loads(res.text)
        user.set_at_event(int(res["at_event"]))
        p = Profile_Layout(user = user,you = self._user,friend = int(res["info"]))
        #vazw to profile
        self.ids.aka.info_layout.add_widget(p)

        return self.manager
#Log In Screen
class First_Screen(Screen):
    usr = None
    mmlayer = None
    to_log = [False,False,False]
    info = {}

    def __init__(self, **kwargs):
        super(First_Screen, self).__init__(**kwargs)
        #vazw ton user
        #gia username text input
        self.ids.aka.us_inp.hint_text = "Username"
        self.ids.aka.us_inp.bind(focus = self.on_focus_username)
        self.ids.aka.us_inp.text = 'Ceidas22'
        #gia email text input
        self.ids.aka.email_inp.hint_text = "E-mail"
        self.ids.aka.email_inp.bind(focus = self.on_focus_email)
        self.ids.aka.email_inp.text = 'ceidas22@gmail.com'
        #gia password inp
        self.ids.aka.passw_inp.hint_text = "Password"
        self.ids.aka.passw_inp.bind(focus = self.on_focus_password)
        self.ids.aka.passw_inp.text = 'Ceid2022!!'
        self.ids.aka.login_bttn.bind(on_press = self.send_info)#8a prepei na stelnw ke coordinates
        self.ids.aka.reg_bttn.bind(on_press = self.send_info_reg)#8a prepei na stelnw ke coordinates
        self.ids.aka.login_bttn.disabled = True#sthn arxh disabled
        self.ids.aka.reg_bttn.disabled = True#sthn arxh disabled

    def on_focus_username(self,instance,focus,**kwargs):
        if focus :
            pass
        else:
            self.check_restrictions()

    def on_focus_email(self,instance,focus,**kwargs):
        if focus :
            pass
        else:
            self.check_restrictions()

    def on_focus_password(self,instance,focus,**kwargs):
        if focus :
            pass
        else:
            self.check_restrictions()

    def check_restrictions(self):
        #gia username
        if len(self.ids.aka.us_inp.text) > 8 :
            self.to_log[0] = True
        else:
            self.to_log[0] = False
        #gia password
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        match_re = re.compile(reg)
        res = re.search(match_re,self.ids.aka.passw_inp.text)
        if res :
            self.to_log[1] = True
        else:
            self.to_log[1] = False
        #gia email
        if (len(self.ids.aka.email_inp.text) > 8) and (".com" in self.ids.aka.email_inp.text) and ("@" in self.ids.aka.email_inp.text):
            self.to_log[2] = True
        else:
            self.to_log[2] = False

        if self.to_log[0] and self.to_log[1] and self.to_log[2]:
            self.ids.aka.login_bttn.disabled = False
            self.ids.aka.reg_bttn.disabled = False
        else:
            self.ids.aka.login_bttn.disabled = True
            self.ids.aka.reg_bttn.disabled = True

    def send_info(self,obj,**kwargs):
        mdict = {
            "msg" : {
                "username":str(self.ids.aka.us_inp.text),
                "password":str(self.ids.aka.email_inp.text),
                "email":str(self.ids.aka.passw_inp.text),
                "coords" : {#'21.795152907519395',38.29040030442736
                    "lat" : 38.290400,
                    "lon" : 21.795153
                }
            }
        }
        mc = myConnection(mdict,'login')
        res = mc.send_dict()
        res = json.loads(res.text)
        if int(res["info"])==1:
            print(str((res["msg"]["id"],res["msg"]["username"],res["msg"]["email"])))
            msc = Second_Screen(name = 'second_light', usr = RegularUser(res["msg"]["id"],res["msg"]["username"],res["msg"]["email"],21.795153,38.290400,res["msg"]["points"],num_of_friends = res["count"][0]["count(*)"]))
            self.manager.add_widget(msc)
            self.manager.current = 'second_light'
            return self.manager
        else:
            #8elw pop up
            popup = Popup(title='Error',content=Label(text=res["msg"]),size_hint=(None, None), size=(235,135))
            popup.open()

    def send_info_reg(self,obj,**kwargs):
        mdict = {
            "msg" : {
                "username":str(self.ids.aka.us_inp.text),
                "password":str(self.ids.aka.email_inp.text),
                "email":str(self.ids.aka.passw_inp.text),
                "coords" : {
                    "lat" : 0,
                    "lon" : 0
                }
            }
        }
        mc = myConnection(mdict,'register')
        res = mc.send_dict()
        res = json.loads(res.text)
        if res["info"] == '1':
            #8elw pop up
            popup = Popup(title='Test popup',content=Label(text="Registered Succesfully!"),size_hint=(None, None), size=(250,145))
            popup.open()
        else :
            #8elw pop up
            popup = Popup(title='Test popup',content=Label(text=res["info"]),size_hint=(None, None), size=(250,145))
            popup.open()

class Main_App(App):

    def build(self):
        #dhmiourgia ScreenManager
        sm = ScreenManager()
        #ta screens tou screen manager
        sm.add_widget(First_Screen(name = 'login_screen'))
        #configure ton screen manager
        sm.current = 'login_screen'
        return sm

Builder.load_file('pointer_app.kv')


def from_Dict_to_User(mdict,current_user,use = 0,frnum=0):#apey8eias opws to stelnei h vash
    if use == 0:
        #8elei allagh
        u =  RegularUser(id = mdict["id"],username = mdict["username"],email = mdict["email"],lon = mdict['lat'], lat = mdict["lat"],points = mdict["points"],pcoins = mdict["pcoins"],online = mdict["online"]["data"])
        if u.get_username() == current_user.get_username():
            return None
        else:
            return u
    else:#hmmm...
        return RegularUser(id = mdict["id"],username = mdict["username"],email = mdict["email"],lon = mdict['lat'], lat = mdict["lat"],points = mdict["points"],pcoins = mdict["pcoins"],online = mdict["online"]["data"],num_of_friends=frnum[0]["count(*)"])

def friends_creation(mdict):
    friends = []
    for i in mdict["info"]:
        friends.append( from_Dict_to_User(mdict = i,current_user = None,use = 1,frnum = mdict["count"].pop(0)) )
    return friends

def friend_request_creation(mdict):
    marr = []
    for i in mdict["info"]:
        marr.append(FriendRequest(id1 = i["id_1"],id2 = i["id_2"],user_1 = i["username_1"],user_2 = i["username_2"],sended = dt.datetime.strptime(i["sended"], "%Y-%m-%dT%H:%M:%S.%f%z"),state_1 = i["state_1"],state_2 = i["state_2"]))
    return marr

if __name__ == "__main__":
    Main_App().run()
