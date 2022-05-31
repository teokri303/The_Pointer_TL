from User import *
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

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image

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

#to main content && ScrollView gia FriendRequests
class FriendsRequLayout(BoxLayout):
    _user = None
    _search_profile_callback = None
    _friendrequest_dict = {}
    def __init__(self,usr,tocallback_profile=None,**kwargs):
        super(FriendsRequLayout, self).__init__(**kwargs)
        #pairnw friend request apo vash
        fr = []
        self._user = usr#apo auto 8a parw info gia friend request
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
#
#Gia tous filous
#
#to main content && ScrollView gia friends
class FriendsLayout(BoxLayout):
    pass
#to main content && ScrollView gia friends
#to main content gia Friends
class Friends_Layout(BoxLayout):
    pass
#to main content gia Friends
#
#Gia tous filous
#
#
#to profile tou xrhsth
#
class Profile_Layout(BoxLayout):

    def __init__(self,**kwargs):
        super(Profile_Layout, self).__init__(**kwargs)
        self.ids.info_layout.online.text = str(self.ids.info_layout.online.text)
        self.ids.info_layout.username.text = str(self.ids.info_layout.username.text)
        self.ids.info_layout.points.text = str(self.ids.info_layout.points.text)
        self.ids.info_layout.friends.text = str(self.ids.info_layout.friends.text)
        self.ids.info_layout.coordinates.text = str(self.ids.info_layout.coordinates.text)
        self.ids.info_layout.friends.text = str(self.ids.info_layout.friends.text)

class Event_Creation_Layout(BoxLayout):

    def __init__(self,**kwargs):
        super(Event_Creation_Layout, self).__init__(**kwargs)
        self.start_spinners()
        self.ids.info_layout.event_datetimes_1.ids.se_label.text = "Start"
        self.ids.info_layout.event_datetimes_2.ids.se_label.text = "End"

    def start_spinners(self):
        #prepei na pairnoun times
        #gia spinners 1
        self.ids.info_layout.event_datetimes_1.ids.spinner_year.values = [str(dt.datetime.today().year) , str(dt.datetime.today().year + 1)]
        self.ids.info_layout.event_datetimes_1.ids.spinner_month.values = list(clnd.month_name[1:])
        x = double_number_function(30)
        self.ids.info_layout.event_datetimes_1.ids.spinner_day.values = x[1:]
        del(x)
        self.ids.info_layout.event_datetimes_1.ids.spinner_hour.values = double_number_function(24)
        self.ids.info_layout.event_datetimes_1.ids.spinner_minute.values = double_number_function(60)

        #gia spinners 2
        self.ids.info_layout.event_datetimes_2.ids.spinner_year.values = [str(dt.datetime.today().year) , str(dt.datetime.today().year + 1)]
        self.ids.info_layout.event_datetimes_2.ids.spinner_month.values = list(clnd.month_name[1:])
        x = double_number_function(30)
        self.ids.info_layout.event_datetimes_2.ids.spinner_day.values = x[1:]
        del(x)
        self.ids.info_layout.event_datetimes_2.ids.spinner_hour.values = double_number_function(24)
        self.ids.info_layout.event_datetimes_2.ids.spinner_minute.values = double_number_function(60)

    def check_restrictions(self):
        try:
            int(self.ids.info_layout.points_loose.text)
            int(self.ids.info_layout.points_earned.text)
            int(self.ids.info_layout.capacity.text)
            #gia diarkeia ti kanw?
            #edw 8elw popup ke 8a to gurnaw se None, auto an den exoun mpei swsta ta datetimes
            if len(self.ids.info_layout.name.text) > 4 and len(self.ids.info_layout.location.text) > 4:
                self.ids.info_layout.subutton.disabled = False
            elif self._creator.get_points() < int(self.ids.info_layout.points_loose.text):
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
            self._to_start_end[self.ids.info_layout.event_datetimes_1.ids.se_label.text] = str(dt.datetime.strptime(dt_value_1, '%Y/%B/%d %H:%M'))
            self._to_start_end[self.ids.info_layout.event_datetimes_2.ids.se_label.text] = str(dt.datetime.strptime(dt_value_2, '%Y/%B/%d %H:%M'))
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


#ta spinner mou
class SpinnerLayout(GridLayout):
    pass
#to main screen
class Second_Screen(Screen):
    _user = None

    def __init__(self,usr ,**kwargs):
        super(Second_Screen, self).__init__(**kwargs)
        self._user = usr
        self._user.set_online(1)
        #prepei na kanw bind tis leitourgies twn koumpiwn
        self.ids.aka.info_layout.map_opp.options_layout.bind(text=self.spinner_selected_value)
        mmap = MapView(zoom=11, lat=25.55, lon=33.32,map_source=MapSource(min_zoom=3))
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
        fr = FriendsRequLayout(usr = self._user)
        self.ids.aka.info_layout.add_widget(fr)
        return self.manager
    #dhmiourgia event
    def create_event(self,instance,**kwargs):#den exw ftiaksei to antistoixo
        self.manager.current = 'second_light'
        #vgazw to map
        self.manager.children[0].ids.aka.info_layout.remove_widget(self.manager.children[0].ids.aka.info_layout.children[0])
        #vazw to profile
        p = Event_Creation_Layout()
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
                "coords" : {
                    "lat" : 38.247344,
                    "lon" : 21.733015
                }
            }
        }
        mc = myConnection(mdict,'login')
        res = mc.send_dict()
        res = json.loads(res.text)
        if int(res["info"])==1:
            msc = Second_Screen(name = 'second_light', usr = User(res["msg"]["username"], res["msg"]["email"],mdict["msg"]["coords"],res["msg"]["points"],id = res["msg"]["id"],num_of_friends = res["count"][0]["count(*)"]))
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

if __name__ == "__main__":
    Main_App().run()
