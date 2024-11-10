from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
import pyrebase
from kivyauth.google_auth import initialize_google, login_google, logout_google
from datetime import datetime
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

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

# Define screen classes
class LoginScreen(Screen):
    pass

class LoginSecondScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class RegistrationScreen(Screen):
    pass

class AdminScreen(Screen):
    pass

class ImunisasiScreen(Screen):
    pass

class RiwayatImunScreen(Screen):
    pass

class ProfilScreen(Screen):
    pass

class PatientItem(BoxLayout):
    name = StringProperty("")
    unique_id = StringProperty("")  # Mengganti balita_id menjadi unique_id
    category = StringProperty("Balita")  # Default kategori untuk balita

class DaftarbalitaScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.load_balita_data, 0.5)  # Schedule to load data after entering the screen

    def load_balita_data(self, *args):
        self.ids.patient_layout.clear_widgets()  # Clear previous list items
        data_balita = db.child("data_balita").get()
        
        if data_balita.each():
            for balita in data_balita.each():
                name = balita.val().get("name", "Unknown")  # Retrieve name
                patient_id = balita.key()  # Unique ID for each record
                
                patient_item = PatientItem(name=name, unique_id=patient_id, category="Balita")
                self.ids.patient_layout.add_widget(patient_item)

    def go_to_imunisasi_screen(self, patient_id):
        # Set any required data for the ImunisasiScreen here
        self.manager.current = 'imunisasi'  # Navigate to Imunisasi screen

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

class HomeApp(Screen):
    def on_enter(self):
        self.fetch_data()

    def fetch_data(self):
        # Memastikan id recycle_view ada di ids
        if 'recycle_view' in self.ids:
            # Hapus data lama di RecycleView
            self.ids.recycle_view.data = []

            # Mengambil data dari tabel lansia
            data_lansia = db.child("lansia").get().val()
            if data_lansia:
                for key, value in data_lansia.items():
                    item = {
                        'nama': value.get('nama', ''),
                        'kategori': 'Lansia',
                    }
                    self.ids.recycle_view.data.append(item)

            # Mengambil data dari tabel balita
            data_balita = db.child("balita").get().val()
            if data_balita:
                for key, value in data_balita.items():
                    item = {
                        'nama': value.get('nama', ''),
                        'kategori': 'Balita',
                    }
                    self.ids.recycle_view.data.append(item)
        else:
            print("ID recycle_view tidak ditemukan di ids.")

class DatabalitaScreen(Screen):
    def on_enter(self):
        # Retrieve data from Firebase
        data_balita = db.child("data_balita").get().val()
        if data_balita:
            # Display data, assuming only one entry is needed
            latest_data = list(data_balita.values())[-1]
            self.ids.tinggi_badan_label.text = f"Tinggi Badan: {latest_data['tinggi_badan']}"
            self.ids.berat_badan_label.text = f"Berat Badan: {latest_data['berat_badan']}"
            self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {latest_data['lingkar_lengan']}"
            self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {latest_data['lingkar_kepala']}"
            self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {latest_data['riwayat_penyakit']}"
            
    def update_data(self, data):
        self.ids.labelNama.text = f"Nama: {data.get('nama', '')}"
        self.ids.tinggi_badan_label.text = f"Tinggi Badan: {data.get('tinggi_badan')}"
        self.ids.berat_badan_label.text = f"Berat Badan: {data.get('berat_badan')}"
        self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {data.get('lingkar_lengan')}"
        self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {data.get('lingkar_kepala')}"
        self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit')}"

class DataLansiaScreen(Screen):
    def on_enter(self):
        # Retrieve data from Firebase
        data_lansia = db.child("data_lansia").get().val()
        if data_lansia:
            # Display data, assuming only one entry is needed
            latest_data = list(data_lansia.values())[-1]
            # Setel data pada label di DataLansiaScreen
            self.ids.labelTinggi.text = f"Tinggi Badan: {latest_data['tinggi_badan']}"
            self.ids.labelBerat.text = f"Berat Badan: {latest_data['berat_badan']}"
            self.ids.labelTekanan.text = f"Tekanan Darah: {latest_data['tekanan_darah']}"
            self.ids.labelGula.text = f"Kadar Gula Darah: {latest_data['gula_darah']}"
            self.ids.labelKolestrol.text = f"Kolestrol: {latest_data['kolestrol']}"
            self.ids.labelRiwayat.text = f"Riwayat Penyakit: {latest_data['riwayat_penyakit']}"
            
    def update_data(self, data):
        self.ids.labelNama.text = f"Nama: {data.get('nama', '')}"
        self.ids.labelTinggi.text = f"Tinggi Badan: {data.get('tinggi_badan')}"
        self.ids.labelBerat.text = f"Berat Badan: {data.get('berat_badan')}"
        self.ids.labelTekanan.text = f"Tekanan Darah: {data.get('tekanan_darah')}"
        self.ids.labelGula.text = f"Kadar Gula Darah: {data.get('gula_darah')}"
        self.ids.labelKolestrol.text = f"Kolestrol: {data.get('kolestrol')}"
        self.ids.labelRiwayat.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit')}"

class AddBalitaScreen(Screen):
    def daftar_balita(self):
        # Collect data from input fields
        data = {
            "tinggi_badan": self.ids.tinggiBadan.text,
            "berat_badan": self.ids.beratBadan.text,
            "lingkar_lengan": self.ids.lingkarLengan.text,
            "lingkar_kepala": self.ids.lingkarKepala.text,
            "riwayat_penyakit": self.ids.riwayatPenyakit.text
        }
        # Push data to Firebase
        db.child("data_balita").push(data)
        print("Data balita has been saved to Firebase.")    

class AddLansiaScreen(Screen):
    def daftar_lansia(self):
        tinggi = self.ids.tinggiBadan.text
        berat = self.ids.beratBadan.text
        tekanan = self.ids.tekananDarah.text
        gula = self.ids.kadarGula.text
        kolesterol = self.ids.kolestrol.text
        riwayat = self.ids.riwayatPenyakit.text

        # Data untuk disimpan
        data = {
            'tinggi_badan': tinggi,
            'berat_badan': berat,
            'tekanan_darah': tekanan,
            'gula_darah': gula,
            'kolestrol': kolesterol,
            'riwayat_penyakit': riwayat
        }

        # Simpan ke Firebase
        app = App.get_running_app()
        app.db.child("data_lansia").push(data)  # Simpan ke Realtime Database

        # Navigasi ke DataLansiaScreen dan muat data
        self.manager.current = 'data'
        self.manager.get_screen('data').load_data()
        
class DaftarScreen(Screen):
    lansia_checkbox = ObjectProperty(None)
    balita_checkbox = ObjectProperty(None)

    def go_to_next_screen(self):
        # Ambil data input dari pengguna
        nik = self.ids.nik.text
        nama = self.ids.nama.text
        tanggal_lahir = self.ids.tanggalLahir.text
        alamat = self.ids.alamat.text
        no_hp = self.ids.noHp.text

        # Buat objek data yang akan disimpan ke Firebase
        data = {
            'nik': nik,
            'nama': nama,
            'tanggal_lahir': tanggal_lahir,
            'alamat': alamat,
            'no_hp': no_hp,
            'timestamp': datetime.now().isoformat()
        }

        # Tentukan jalur penyimpanan di Firebase berdasarkan kategori
        if self.lansia_checkbox.active:
            App.get_running_app().firebase_db.child("lansia").push(data)
            self.manager.current = "addlansia"
        elif self.balita_checkbox.active:
            App.get_running_app().firebase_db.child("balita").push(data)
            self.manager.current = "addbalita"
        
    def submit_form(self):
        # Ambil data dari form input
        nama = self.ids.nama_input.text
        kategori = self.ids.kategori_input.text
        
        # Tambahkan data ke RecycleView
        app = App.get_running_app()
        app.add_data(nama, kategori)
        
        # Bersihkan form input setelah submit
        self.ids.nama_input.text = ''
        self.ids.kategori_input.text = ''
        
        # Pindah ke halaman home setelah submit
        self.manager.current = "home"

class QueueScreen(Screen):
    def on_enter(self):
        # Tampilkan nomor antrian yang diambil
        nomor_antrian = db.child("nomor_antrian").child(self.get_current_user_id()).get().val() or []
        self.ids.taken_queue_label.text = "\n".join(nomor_antrian)

    def get_current_user_id(self):
        # Mengambil current user dari objek auth
        user = auth.current_user  # Mengakses auth dari main
        return user['localId'] if user else None

    def get_user_name(self):
        # Mendapatkan nama pengguna dari profil pengguna
        user = auth.current_user  # Mengakses auth dari main
        return user['displayName'] if user and 'displayName' in user else "User Tanpa Nama"

    def get_queue(self):
        user_id = self.get_current_user_id()
        nomor_antrian = db.child("nomor_antrian").child(user_id).get().val() or []

        if len(nomor_antrian) < 2:  # Cek jika sudah mengambil 2 antrian
            count = db.child("queue/count").get().val()
            if count and count > 0:
                queue_number = count
                db.child("queue").update({"count": count - 1})

                user_name = self.get_user_name()  # Ambil nama pengguna
                nomor_antrian.append(f"{user_name}: Antrian {queue_number}")  # Simpan dengan nama

                try:
                    db.child("nomor_antrian").child(user_id).set(nomor_antrian)  # Simpan ke nomor_antrian
                    self.ids.queue_label.text = f"Antrian Diambil, Nomor: {queue_number}"
                except Exception as e:
                    self.ids.queue_label.text = f"Gagal mengambil antrian: {e}"
            else:
                self.ids.queue_label.text = "Antrian Habis"
        else:
            self.ids.queue_label.text = "Anda sudah mengambil 2 antrian."
            
class AdminAntrianScreen(Screen):
    def on_enter(self):
        # Ambil jumlah antrian dari database saat masuk
        count = db.child("queue/count").get().val()
        self.ids.queue_label.text = f"Jumlah Antrian: {count}"

    def update_queue(self):
        # Ambil jumlah dari input, update ke database
        count = int(self.ids.queue_input.text)
        db.child("queue").update({"count": count})
        self.ids.queue_label.text = f"Jumlah Antrian: {count}"

    def show_nomor_antrian(self):
        # Ambil semua antrian yang telah diambil oleh semua pengguna
        nomor_antrian = db.child("nomor_antrian").get().val()
        if nomor_antrian:
            display_text = ""
            for user_id, queues in nomor_antrian.items():
                for queue in queues:
                    display_text += f"User ID: {user_id}, Antrian: {queue}\n"
            self.ids.taken_queue_label.text = display_text
        else:
            self.ids.taken_queue_label.text = "Belum ada antrian yang diambil."
    def show_remaining_queue(self):
        # Menampilkan sisa antrian di admin
        remaining_count = db.child("queue/count").get().val()
        self.ids.remaining_queue_label.text = f"Sisa Antrian: {remaining_count}"

class PatientItem(BoxLayout):
    name = StringProperty()
    category = StringProperty()

    def __init__(self, name, category, **kwargs):
        super(PatientItem, self).__init__(**kwargs)
        self.name = name
        self.category = category

class PatientList(Screen):
    def __init__(self, **kwargs):
        super(PatientList, self).__init__(**kwargs)

        # Data pasien
        self.patients = [
            ("Rohmad Rafi N", "Lansia"),
            ("Musarof Morisorona", "Balita"),
            ("Anggit Hardianto", "Lansia"),
            ("Otto Santoso P", "Balita"),
            ("Syahrul Ageng P", "Lansia"),
            ("Irfan Ramadhan", "Balita"),
            ("Taufiq Fadhly R", "Lansia"),
            ("Bagas Fitriandra", "Balita")
        ]

    def on_pre_enter(self):
        # Display initial list of patients
        self.update_patient_list("All")

    def update_patient_list(self, category):
        self.ids.patient_layout.clear_widgets()
        for name, patient_category in self.patients:
            if category == "All" or patient_category == category:
                patient_box = PatientItem(name=name, category=patient_category)
                self.ids.patient_layout.add_widget(patient_box)

class UserItem(BoxLayout):
    name = StringProperty()
    category = StringProperty()

    def __init__(self, name, category, **kwargs):
        super(UserItem, self).__init__(**kwargs)
        self.name = name
        self.category = category

class UserList(Screen):
    def __init__(self, **kwargs):
        super(UserList, self).__init__(**kwargs)

        # Data pasien
        self.users = [
            ("Rohmad Rafi N", "rafi@gmail.com"),
            ("Musarof Morisorona", "rona@gmail.com"),
            ("Anggit Hardianto", "anggit@gmail.com"),
            ("Otto Santoso P", "otto@gmail.com"),
            ("Syahrul Ageng P", "arul@gmail.com"),
            ("Irfan Ramadhan", "irfn@gmail.com"),
            ("Taufiq Fadhly R", "dlyy@gmail.com"),
            ("Bagas Fitriandra", "bgskn@gmail.com")
        ]

    def on_pre_enter(self):
        # Display initial list of patients
        self.update_user_list("All")

    def update_user_list(self, category):
        self.ids.user_layout.clear_widgets()
        for name, user_category in self.users:
            if category == "All" or user_category == category:
                user_box = UserItem(name=name, category=user_category)
                self.ids.user_layout.add_widget(user_box)
                
class ClickableBox(ButtonBehavior, BoxLayout):
    def __init__(self, user_data, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data

    def on_press(self):
        app = App.get_running_app()
        app.root.current = 'home'
        app.root.get_screen('home').ids.welcome_label.text = f"Welcome, {self.user_data.get('name')}"

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
