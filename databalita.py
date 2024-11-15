from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen
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

class DatabalitaApp(App):
    def build(self):
        kv_files = ['databalita.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DatabalitaScreen()

class DatabalitaScreen(Screen):
    def on_enter(self):
        # Retrieve data from Firebase
        data_balita = db.child("data_balita").get().val()
        if data_balita:
            # Display data, assuming only one entry is needed
            selected_data = list(data_balita.values())[-1]
            self.ids.tinggi_badan_label.text = f"Tinggi Badan: {selected_data['tinggi_badan']}"
            self.ids.berat_badan_label.text = f"Berat Badan: {selected_data['berat_badan']}"
            self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {selected_data['lingkar_lengan']}"
            self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {selected_data['lingkar_kepala']}"
            self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {selected_data['riwayat_penyakit']}"
            
    def update_data(self, data):
        self.ids.labelNama.text = f" {data.get('nama', '')}"
        self.ids.tinggi_badan_label.text = f"Tinggi Badan: {data.get('tinggi_badan')}"
        self.ids.berat_badan_label.text = f"Berat Badan: {data.get('berat_badan')}"
        self.ids.lingkar_lengan_label.text = f"Lingkar Lengan Atas: {data.get('lingkar_lengan')}"
        self.ids.lingkar_kepala_label.text = f"Lingkar Kepala: {data.get('lingkar_kepala')}"
        self.ids.riwayat_penyakit_label.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit')}"

if __name__ == '__main__':
    DatabalitaApp().run()
