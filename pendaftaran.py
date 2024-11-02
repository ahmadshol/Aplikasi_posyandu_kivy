from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.lang import Builder
import os
import pyrebase
from kivy.properties import ObjectProperty

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

class AddBalitaScreen(Screen):
    pass

class AddLansiaScreen(Screen):
    pass

class DaftarScreen(Screen):
    lansia_checkbox = ObjectProperty(None)
    balita_checkbox = ObjectProperty(None)

    def go_to_next_screen(self):
        if self.lansia_checkbox.active:
            self.manager.current = 'addlansia'
        elif self.balita_checkbox.active:
            self.manager.current = 'addbalita'
        else:
            # Anda mungkin ingin menambahkan alert atau penanganan error di sini
            print("Silakan pilih Lansia atau Balita.")

class daftarApp(App):
    def build(self):
        kv_files = ['pendaftaran.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DaftarScreen()
    
if __name__ == '__main__':
    daftarApp().run()
