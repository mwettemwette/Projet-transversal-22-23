import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder 
from kivymd.theming import ThemeManager
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

import lecture_base as lbdd


kivy.require("1.9.1")

def popup():
    show=P()
    pop = Popup(title="user not found", content=show, size=(200,200))
    pop.open()

class P(FloatLayout):
    pass

class MyScreenManager(ScreenManager):
    def show_popup(self):
        popup = CustomPopup(title='test', message='popup test')
        popup.open()

class In_the_queue(Screen):
    """ The window running when the user is logged """
    def display_info(self, sender, adresse):
        self.ids.sender.text = sender
        self.ids.adresse.text = adresse

  
class Logged_in(Screen):
    """ The window running when the user is logged """
    def welcome_user(self, text):
        self.ids.user.text = f"Welcome {text}"
        self.ids.sender.text=text


    def call_robot(self):
        adresse = self.ids.adresse.text
        sender = self.ids.sender.text
        if lbdd.write_call(sender, adresse):
            print("robot called")
            self.manager.get_screen('In_the_queue').display_info(sender, adresse)
            self.clear_inputs()
            return True
    def clear_inputs(self):
        self.ids.adresse.text = ""


class Log(Screen, Widget):
    """ The window displayed whane the user has to log in """
    def log_error(self):
        popup()    

    def logged_in(self):
        user_name = self.ids.user_id.text
        user_pwd = self.ids.user_pwd.text
        print("connecting")
        if (lbdd.check_utilisateur(user_name, user_pwd) ):
            print(f"Connected ! : {user_name} ")
            print("redirecting to the log in window")
            self.manager.get_screen('Logged_in').welcome_user(user_name)
            self.clear_inputs()
            return True
        else :
            return False


    def clear_inputs(self):
        self.ids.user_id.text = ""
        self.ids.user_pwd.text = ""
    
    pass

class Accueil(Screen):
    """ The window displayed by default on the app """
    pass

        
class MainApp(App):
    
    
    def change_window(self, nom_fenetre, direction='avant', mode="", diration="0.5"):
        screen_manager=self.root.ids["screen_manager"]

        if direction=='avant':
            mode='push'
            direction='left' 

        elif direction=='arriere':
            mode='pop'
            direction='right'  
        screen_manager.transition= CardTransition(direction=direction, mode=mode, duration = duration)
        screen_manager.current= nom_fenetre


        
    def build(self):
        sm = MyScreenManager()

        # Création des fenêtres
        accueil = Accueil(name='Accueil')
        log = Log(name='Log')
        logged= Logged_in(name='Logged_in')
        queue_win = In_the_queue(name='In_the_queue')

        

        sm.add_widget(accueil)
        sm.add_widget(log)
        sm.add_widget(logged)
        sm.add_widget(queue_win)


        return sm   #self.running_window #lst_window[1] #Builder.load_file("appli.kv")


if __name__ == '__main__':
     
    Builder.load_file('robot.kv')
    MainApp().run()
