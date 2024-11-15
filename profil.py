from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen
import pyrebase

Window.size = (360, 640)

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyBtXAFglMuV2PN2hAS6mEYPyFU6H_qSBEQ",
    "authDomain": "kesehatan-masyarakat.firebaseapp.com",
    "databaseURL": "https://kesehatan-masyarakat-default-rtdb.firebaseio.com",
    "projectId": "kesehatan-masyarakat", 
    "storageBucket": "kesehatan-masyarakat.appspot.com",
    "messagingSenderId": "366757069189",
    "appId": "1:366757069189:web:44b18a06d3b38b862584ec",
    "measurementId": "G-W29SS10Z7Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

class ProfilApp(App):
    def build(self):
        kv_files = ['profil.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return ProfilScreen()
    

class ProfilScreen(Screen):
    def display_name(self, name):
        print("Nama:", name)
        if name:
            self.ids.name_label_1.text = name
            self.ids.name_label_2.text = name
        else:
            print("Nama tidak tersedia")
            self.ids.name_label_1.text = "Nama tidak tersedia"
            self.ids.name_label_2.text = "Nama tidak tersedia"

    def display_email(self, email):
        print("Email:", email)
        if email:
            self.ids.email_label.text = email
        else:
            print("Email tidak tersedia")
            self.ids.email_label.text = "Email tidak tersedia"


if __name__ == '__main__':
    ProfilApp().run()
