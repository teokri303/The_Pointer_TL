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
from kivy.uix.image import Image
from functools import partial

from kivy.uix.screenmanager import ScreenManager, Screen
#gia map
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy_garden.mapview import MapSource


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
        self.ids.aka.us_inp.bind(focus = self.on_my_focus)
        #gia email text input
        self.ids.aka.email_inp.hint_text = "E-mail"
        self.ids.aka.email_inp.bind(focus = self.on_my_focus)
        #gia password inp
        self.ids.aka.passw_inp.hint_text = "Password"
        self.ids.aka.passw_inp.bind(focus = self.on_my_focus)
        self.ids.aka.login_bttn.bind(on_press = self.to_main_screen)#8a prepei na stelnw ke coordinates
        self.ids.aka.login_bttn.disabled = True#sthn arxh disabled
        self.ids.aka.reg_bttn.disabled = True#sthn arxh disabled

    def on_my_focus(self,instance,focus,**kwargs):
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

    def to_main_screen(self,obj,**kwargs):
        msc = Second_Screen(name = 'second_light')
        self.manager.add_widget(msc)
        self.manager.current = 'second_light'
        return self.manager

class Second_Screen(Screen):

    def __init__(self,**kwargs):
        super(Second_Screen, self).__init__(**kwargs)
        mmap = MapView(zoom=11, lat=64.64, lon=37.37,map_source=MapSource(min_zoom=3))
        #vazw map
        self.ids.aka.info_layout.add_widget(mmap)

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
