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
    "appId": "1:366757069189:web:44b18a06d3b38b862584ec"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

Window.size = (360, 640)

class ImunisasiApp(App):
    def build(self):
        kv_files = ['imunisasi.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return ImunisasiScreen()

class ImunisasiScreen(Screen):
    def on_enter(self):
        # Retrieve data from Firebase
        data_balita = db.child("data_balita").get().val()
        if data_balita:
            # Ambil data terbaru (bisa sesuaikan berdasarkan kondisi data Anda)
            latest_data = list(data_balita.values())[-1]
            
            # Update tampilan dengan data yang ada
            if 'nama' in latest_data:
                self.ids.labelNama.text = f"Nama: {latest_data['nama']}"
            if 'tinggi_badan' in latest_data:
                self.ids.tinggi_badan_label.text = f"Tinggi Badan: {latest_data['tinggi_badan']}"
            if 'berat_badan' in latest_data:
                self.ids.berat_badan_label.text = f"Berat Badan: {latest_data['berat_badan']}"
            if 'lingkar_lengan' in latest_data:
                self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {latest_data['lingkar_lengan']}"
            if 'lingkar_kepala' in latest_data:
                self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {latest_data['lingkar_kepala']}"
            if 'riwayat_penyakit' in latest_data:
                self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {latest_data['riwayat_penyakit']}"
            
    def update_data(self, data):
        # Update data yang diterima
        self.ids.labelNama.text = f"Nama: {data.get('nama', 'Tidak ada nama')}"
        self.ids.tinggi_badan_label.text = f"Tinggi Badan: {data.get('tinggi_badan', 'Tidak ada data')}"
        self.ids.berat_badan_label.text = f"Berat Badan: {data.get('berat_badan', 'Tidak ada data')}"
        self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {data.get('lingkar_lengan', 'Tidak ada data')}"
        self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {data.get('lingkar_kepala', 'Tidak ada data')}"
        self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit', 'Tidak ada data')}"

class RiwayatImunScreen(Screen):
    pass

class DaftarbalitaScreen(Screen):
    def on_enter(self):
        # Ketika layar dibuka, panggil fungsi untuk mengambil data balita
        self.fetch_balita_data()

    def fetch_balita_data(self):
        try:
            # Mengambil data dari "data_balita" di Realtime Database
            balita_data = db.child("balita").get()

            # Hapus daftar balita sebelumnya di UI
            self.ids.patient_layout.clear_widgets()

            # Iterasi data balita dan tambahkan ke UI
            for item in balita_data.each():
                data = item.val()
                # Setel kategori langsung ke "Balita"
                balita_widget = Balitalist(name=data['nama'], category="Balita")
                self.ids.patient_layout.add_widget(balita_widget)

        except Exception as e:
            print("Error fetching data:", e)
            
class Balitalist(BoxLayout):
    name = StringProperty()
    category = StringProperty()
    
    def go_to_imunisasi(self):
        # Arahkan ke screen imunisasi
        app = App.get_running_app()
        app.root.current = 'imun'

if __name__ == '__main__':
    ImunisasiApp().run()
