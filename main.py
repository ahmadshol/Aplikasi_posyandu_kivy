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
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.clock import Clock
# Screen
from home import HomeApp, UserApp
from datauser import UserList, UserApp, EditUserScreen
from antrian import QueueScreen, QueueApp
from admin import AdminApp, AdminScreen
from profil import ProfilApp, ProfilScreen
from datapasien import PatientList, PatientApp, PatientItem, EditPatientScreen
from databalita import DatabalitaScreen, DatabalitaApp
from login import LoginScreen, LoginSecondScreen, HealthApp
from registrasi import RegistrationScreen, RegistrationApp
from adminantrian import AdminAntrianApp, AdminAntrianScreen
from pendaftaran import AddBalitaScreen, DaftarScreen, daftarApp
from imunisasi import ImunisasiApp, ImunisasiScreen, RiwayatImunScreen
# Firebase configuration
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

# Set window size for mobile-like experience
Window.size = (360, 640)

# Custom widget classes
class BoxRounded(BoxLayout):
    pass

class ClickableImage(ButtonBehavior, Image):
    pass

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
        if self.kategori == 'Balita':
            data_screen = app.root.get_screen('databalita')
            app.root.current = 'databalita'
        elif self.kategori == 'Lansia':
            data_screen = app.root.get_screen('data')
            app.root.current = 'data'
            
            

        # Mengirim data ke layar detail yang sesuai
        data_screen.update_data(selected_data)

class MyApp(App):
    def build(self):
        kv_files = ['main.kv','admin.kv','adminantrian.kv','antrian.kv','databalita.kv','home.kv','imunisasi.kv','login.kv','pendaftaran.kv','profil.kv','registrasi.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        # Buat ScreenManager dan tambahkan layar
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='page_one'))
        self.sm.add_widget(LoginSecondScreen(name='page_two'))
        self.sm.add_widget(HomeApp(name='home'))
        self.sm.add_widget(RegistrationScreen(name='registrasi'))
        self.sm.add_widget(AdminScreen(name='admin'))
        self.sm.add_widget(QueueScreen(name='antrian'))
        self.sm.add_widget(DaftarScreen(name='daftar'))
        self.sm.add_widget(PatientList(name='pasien'))
        self.sm.add_widget(UserList(name='datauser'))
        self.sm.add_widget(ImunisasiScreen(name='imun'))
        self.sm.add_widget(DatabalitaScreen(name='databalita'))
        self.sm.add_widget(AdminAntrianScreen(name='admantrian'))
        self.sm.add_widget(RiwayatImunScreen(name='riwayatimun'))
        self.sm.add_widget(AddBalitaScreen(name='addbalita'))
        self.sm.add_widget(ProfilScreen(name='profil'))
        self.sm.add_widget(EditPatientScreen(name='edit_patient'))
        self.sm.add_widget(EditUserScreen(name='edit_user'))

        # Set layar awal ke login
        self.sm.current = 'page_two'
        
        
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
            "appId": "1:366757069189:web:44b18a06d3b38b862584ec",
            "measurementId": "G-W29SS10Z7Q"

        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
        self.firebase_db = firebase.database()
        return self.sm

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
            if user:
                app = App.get_running_app()
                app.user_id = user['localId']
                app.id_token = user['idToken']

                # Ambil data pengguna
                users_ref = db.child("users").child(app.user_id).get(token=app.id_token)
                if users_ref.val():
                    user_data = users_ref.val()
                    name = user_data.get("name", "Nama tidak ada")
                    email = user_data.get("email", "Email tidak ada")
                    
                    # Tampilkan data pengguna setelah sedikit penundaan untuk memastikan layar profil siap
                    Clock.schedule_once(lambda dt: self.update_profil_screen(name, email))
                    
                    # Navigasi berdasarkan role
                    role = user_data.get("role")
                    if role == "admin":
                        self.root.current = 'admin'
                    elif role == "user":
                        self.root.current = 'profil'
                    else:
                        print("Role tidak ditemukan")
                else:
                    print("Data pengguna tidak ditemukan.")
            else:
                raise Exception("Login gagal, data pengguna tidak ditemukan.")
        except Exception as e:
            print("Login Error:", e)

    def update_profil_screen(self, name, email):
        profil_screen = self.root.get_screen('profil')
        profil_screen.display_name(name)
        profil_screen.display_email(email)

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
    
    def get_current_user_id(self):
        user = auth.current_user
        return user['localId'] if user else None   

    def on_pre_enter(self):
        self.update_user_list()

    def update_user_list(self):
        self.ids.user_layout.clear_widgets()
        users = db.child("users").get().val()
        if users:
            for user_id, user_data in users.items():
                user_box = UserItem(user_id=user_id, name=user_data["name"], email=user_data["email"])
                self.ids.user_layout.add_widget(user_box)

if __name__ == '__main__':
    MyApp().run()
