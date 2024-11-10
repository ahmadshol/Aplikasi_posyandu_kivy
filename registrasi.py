from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.popup import Popup
import pyrebase
from kivy.uix.screenmanager import ScreenManager, Screen

# Initialize Firebase
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

class RegistrationScreen(Screen):
    pass

class RegistrationApp(App):
    def build(self):
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv','registrasi.kv')
        Builder.load_file(kv_file_path)
        return RegistrationScreen()

    def register(self, name, email, password, role):
        try:
            # Firebase registration
            user = auth.create_user_with_email_and_password(email, password)

            # Get user token
            id_token = user['idToken']

            # Save user data to Realtime Database
            db.child("users").child(user['localId']).set({
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }, token=id_token)

            popup = Popup(title='Registration Successful', content=Label(text=f'Registration successful for {role}'), size_hint=(None, None), size=(400, 200))
            popup.open()
        except Exception as e:
            popup = Popup(title='Registration Failed', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200))
            popup.open()

if __name__ == '__main__':
    RegistrationApp().run()
