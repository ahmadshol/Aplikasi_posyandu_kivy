from kivy.app import App
import pyrebase
import os
from datetime import datetime
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivyauth.google_auth import initialize_google, login_google, logout_google
from login import LoginScreen, LoginSecondScreen, HealthApp
from registrasi import RegistrationScreen, RegistrationApp
from admin import AdminApp, AdminScreen
from imunisasi import ImunisasiApp, ImunisasiScreen, RiwayatImunScreen, DaftarbalitaScreen
from profil import ProfilApp, ProfilScreen
from home import HomeApp, UserApp
from databalita import DatabalitaScreen, DatabalitaApp
from datalansia import DataLansiaScreen, DataLansiaApp
from pendaftaran import AddBalitaScreen, AddLansiaScreen, DaftarScreen, daftarApp
from antrian import QueueScreen, QueueApp
from adminantrian import AdminAntrianApp, AdminAntrianScreen
from datapasien import PatientList, PatientApp
from datauser import UserList, UserApp

# Firebase configuration
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

# Set window size for mobile-like experience
Window.size = (360, 640)

# Custom widget classes
class BoxRounded(BoxLayout):
    pass

class ClickableImage(ButtonBehavior, Image):
    pass

class MyScreenManager(ScreenManager):
    pass

class Balitalist(BoxLayout):
    name = StringProperty()
    category = StringProperty()
    
    def go_to_imunisasi(self):
        # Arahkan ke screen imunisasi
        app = App.get_running_app()
        app.root.current = 'imun'

class ClickBox(ButtonBehavior, RecycleDataViewBehavior, BoxLayout):
    nama = StringProperty("")
    kategori = StringProperty("")

    def navigate_to_screen(self):
        # Data contoh untuk menampilkan data lansia/balita
        # Ganti dengan logika pengambilan data dari Firebase
        selected_data = {
            "nama": self.nama,
            "kategori": self.kategori,
            "tinggi_badan": "160 cm",
            "berat_badan": "65 kg",
            "tekanan_darah": "120/80 mmHg",
            "kadar_gula": "90 mg/dL",
            "kolesterol": "180 mg/dL",
            "riwayat_penyakit": "Hipertensi"
        }

        # Menentukan layar yang akan dituju berdasarkan kategori
        app = App.get_running_app()
        if self.kategori == 'Lansia':
            data_screen = app.root.get_screen('data')
            app.root.current = 'data'
        elif self.kategori == 'Balita':
            data_screen = app.root.get_screen('databalita')
            app.root.current = 'databalita'

        # Mengirim data ke layar detail yang sesuai
        data_screen.update_data(selected_data)

class PatientItem(BoxLayout):
    name = StringProperty()
    category = StringProperty()

    def __init__(self, name, category, **kwargs):
        super(PatientItem, self).__init__(**kwargs)
        self.name = name
        self.category = category
        
class UserItem(BoxLayout):
    name = StringProperty()
    category = StringProperty()

    def __init__(self, name, category, **kwargs):
        super(UserItem, self).__init__(**kwargs)
        self.name = name
        self.category = category

class MyApp(App):
    def build(self):
        kv_files = ['main.kv', 'home.kv', 'login.kv', 'registrasi.kv', 'admin.kv','antrian.kv',
                    'datalansia.kv','pendaftaran.kv','datapasien.kv','datauser.kv','imunisasi.kv',
                    'databalita.kv','adminantrian.kv', 'profil.kv']
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
            client_id = open("json/client_id.txt")
            client_secret = open("json/client_secret.txt")
            initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
            
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
        self.db = firebase.database()
        self.firebase_db = firebase.database()
        return MyScreenManager()

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
        
    def login(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_screen = self.root.get_screen('page_two')
            login_screen.user = user
            id_token = user['idToken']
            users_ref = db.child("users").child(user['localId']).get(token=id_token)
            if users_ref.val():
                user_data = users_ref.val()
                role = user_data.get("role")
                if role == "admin":
                    self.root.current = 'admin'
                elif role == "user":
                    self.root.current = 'home'
                else:
                    Popup(title='Error', content=Label(text='Role not found'), size_hint=(None, None), size=(400, 200)).open()
            else:
                Popup(title='Error', content=Label(text='User data not found'), size_hint=(None, None), size=(400, 200)).open()
        except Exception as e:
            Popup(title='Login Error', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200)).open()

    def register(self, name, email, password, role):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            registrasi_screen = self.root.get_screen('registrasi')
            registrasi_screen.user = user
            id_token = user['idToken']
            db.child("users").child(user['localId']).set({
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }, token=id_token)
            Popup(title='Registration Successful', content=Label(text=f'Registration successful for {role}'), size_hint=(None, None), size=(400, 200)).open()
        except Exception as e:
            Popup(title='Registration Failed', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200)).open()
        
    def submit_form(self, nama, kategori):
        # Data dari form
        data = {
            "nama": nama,
            "kategori": kategori
        }
        
        # Mengirim data ke Firebase Realtime Database
        db.child("pendaftaran").push(data)
        print("Data berhasil dikirim ke Firebase")

        # Pindah ke halaman home setelah mengirim data
        self.root.current = 'home'    
        
    def add_data(self, nama, kategori):
        # Menambahkan data baru setelah form pendaftaran
        self.data.append({"nama": nama, "kategori": kategori})
        self.update_recycleview()

    def update_recycleview(self):
        # Update RecycleView dengan data terbaru
        self.root.ids.recycle_view.data = self.data    

if __name__ == '__main__':
    MyApp().run()
