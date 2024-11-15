from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
import pyrebase

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

Window.size = (360, 640)


class MyScreenManager(ScreenManager):
    pass

class ImunisasiScreen(Screen):
    data_balita_list = []  # Simpan daftar data balita

    def on_enter(self):
        # Retrieve all data from Firebase
        data_balita = db.child("data_balita").get().val()
        if data_balita:
            # Simpan semua data dalam list untuk referensi
            self.data_balita_list = list(data_balita.values())
            
            # Tampilkan daftar nama balita dalam spinner atau daftar lainnya
            self.populate_spinner([item.get('nama', 'Tidak diketahui') for item in self.data_balita_list])

    def populate_spinner(self, names):
        # Populasi spinner atau daftar dengan nama balita
        self.ids.balita_spinner.values = names

    def on_balita_selected(self, selected_name):
        # Cari data berdasarkan nama yang dipilih
        for data in self.data_balita_list:
            if data.get('nama') == selected_name:
                # Tampilkan detail data balita
                self.update_data(data)
                break

    def update_data(self, data):
        # Update data yang dipilih
        self.ids.labelNama.text = f"Nama: {data.get('nama', 'Tidak ada nama')}"
        self.ids.tinggi_badan_label.text = f"Tinggi Badan: {data.get('tinggi_badan', 'Tidak ada data')}"
        self.ids.berat_badan_label.text = f"Berat Badan: {data.get('berat_badan', 'Tidak ada data')}"
        self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {data.get('lingkar_lengan', 'Tidak ada data')}"
        self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {data.get('lingkar_kepala', 'Tidak ada data')}"
        self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit', 'Tidak ada data')}"

class RiwayatImunScreen(Screen):
    pass

class ImunisasiApp(App):
    def build(self):
        kv_files = ['imunisasi.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return ImunisasiScreen()
    
if __name__ == '__main__':
    ImunisasiApp().run()
