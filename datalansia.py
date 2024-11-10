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
    "appId": "1:366757069189:web:44b18a06d3b38b862584ec"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

Window.size = (360, 640)

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
        self.ids.labelNama.text = f" {data.get('nama', '')}"
        self.ids.labelTinggi.text = f"Tinggi Badan: {data.get('tinggi_badan')}"
        self.ids.labelBerat.text = f"Berat Badan: {data.get('berat_badan')}"
        self.ids.labelTekanan.text = f"Tekanan Darah: {data.get('tekanan_darah')}"
        self.ids.labelGula.text = f"Kadar Gula Darah: {data.get('gula_darah')}"
        self.ids.labelKolestrol.text = f"Kolestrol: {data.get('kolestrol')}"
        self.ids.labelRiwayat.text = f"Riwayat Penyakit: {data.get('riwayat_penyakit')}"
            
class DataLansiaApp(App):
    def build(self):
        kv_files = ['datalansia.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DataLansiaScreen()



if __name__ == '__main__':
    DataLansiaApp().run()
