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
    def daftar_balita(self):
        # Collect data from input fields
        data = {
            "nama": self.ids.nama.text,
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

class daftarApp(App):
    def build(self):
        kv_files = ['pendaftaran.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DaftarScreen()
    
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
    
if __name__ == '__main__':
    daftarApp().run()
