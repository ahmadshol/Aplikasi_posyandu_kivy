from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.lang import Builder
import os
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBtXAFglMuV2PN2hAS6mEYPyFU6H_qSBEQ",
    "authDomain": "kesehatan-masyarakat.firebaseapp.com",
    "databaseURL": "https://kesehatan-masyarakat-default-rtdb.firebaseio.com",
    "projectId": "kesehatan-masyarakat", 
    "storageBucket": "kesehatan-masyarakat.appspot.com",
    "messagingSenderId": "366757069189",
    "appId": "1:366757069189:web:44b18a06d3b38b862584ec"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

Window.size = (360, 640)

class MyScreenManager(ScreenManager):
    pass

class LoginScreen(Screen):
    pass

class LoginSecondScreen(Screen):
    pass

class HealthApp(App):
    def build(self):
        kv_files = ['login.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        client_id = open("json/client_id.txt")
        client_secret = open("json/client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
        return MyScreenManager()

    def login(self, email, password):
        try:
            # Firebase login
            user = auth.sign_in_with_email_and_password(email, password)

            # Get user token
            id_token = user['idToken']

            # Retrieve user role from database
            user_data = db.child("users").child(user['localId']).get(token=id_token).val()
            role = user_data.get("role", "")

            if role == "admin":
                self.root.current = 'admin'  # Switch to admin screen
            else:
                self.root.current = 'home'  # Switch to home screen
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200))
            popup.open()

    def after_login(self, name, email, photo_uri):
        account_screen = self.root.get_screen('page_one')  # Mendapatkan instance AccountScreen
        account_screen.ids.label.text = f"logged as {name}"
        self.root.transition.direction = "left"
        self.root.current = "home"
        
    def error_listener(self):
        print("loggin failed!!!")
    
    def loginn(self):
        login_google()
        
    def logout(self):
        logout_google(self .after_logout())
        
    def after_logout(self):
        self.root.ids.label.text = ""
        self.root.ids.transition.direction = "right"
        self.root.current = "page_one"

if __name__ == '__main__':
    HealthApp().run()
