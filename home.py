from kivy.config import Config
import os
import pyrebase
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

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
        
# Set the window size
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

class MyScreenManager(ScreenManager):
    pass

class HomeApp(Screen):
    def on_enter(self):
        self.fetch_data()

    def fetch_data(self):
        # Memastikan id recycle_view ada di ids
        if 'recycle_view' in self.ids:
            # Hapus data lama di RecycleView
            self.ids.recycle_view.data = []

            # Mengambil data pasien berdasarkan nama dari tabel 'balita'
            data_balita = db.child("data_balita").order_by_child("nama").get().val()

            if data_balita:
                for key, value in data_balita.items():
                    item = {
                        'nama': value.get('nama', ''),
                        'kategori': 'Balita',
                    }
                    # Menambahkan item ke data recycle_view
                    self.ids.recycle_view.data.append(item)
            else:
                print("Data balita tidak ditemukan.")
        else:
            print("ID recycle_view tidak ditemukan di ids.")
            
        user_id = App.get_running_app().get_current_user_id()
        
        if user_id:
            nomor_antrian = db.child("nomor_antrian").child(user_id).get().val() or []
            self.update_queue_label(nomor_antrian)
        else:
            self.ids.home_queue_label.text = "User tidak ditemukan."

        # perbaikan pembacaan berdasarkan nama di tabel
    # def display_queue(self, queue_number):
    #     print("antrian:", queue_number)
    #     if queue_number:
    #         self.ids.queue_label_1.text = queue_number
    #     else:
    #         print("antrian tidak tersedia")
    #         sself.ids.queue_label_1.text = "antrian tidak tersedia"
    def update_queue_label(self, nomor_antrian):
        if nomor_antrian:
            self.ids.home_queue_label.text = "\n".join(nomor_antrian)
        else:
            self.ids.home_queue_label.text = "Belum ada nomor antrean yang diambil."
            
            
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

class UserApp(App):
    def build(self):
        # Ensure the path to the kv file is correct
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv','home.kv')
        Builder.load_file(kv_file_path)
        return HomeApp()
    
    def update_recycleview(self):
        # Update RecycleView dengan data terbaru
        self.root.ids.recycle_view.data = self.data
    
    def on_enter(self):
        self.fetch_data()  # Mengambil data pasien untuk RecycleView
        self.fetch_queue_data()  # Mengambil nomor antrian dan menampilkannya

    def fetch_data(self):
        # Memastikan id recycle_view ada di ids
        if 'recycle_view' in self.ids:
            # Hapus data lama di RecycleView
            self.ids.recycle_view.data = []

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

    def fetch_queue_data(self):
        user_id = self.get_current_user_id()  # Mendapatkan ID pengguna saat ini
        if user_id:
            nomor_antrian = db.child("nomor_antrian").child(user_id).get().val() or []
            if nomor_antrian:
                self.update_queue_display(nomor_antrian)  # Memperbarui label dengan nomor antrian
            else:
                self.ids.home_queue_label.text = "Anda belum mengambil antrian."
        else:
            self.ids.home_queue_label.text = "User tidak ditemukan."

    def get_current_user_id(self):
        user = auth.current_user
        return user['localId'] if user else None     

if __name__ == '__main__':
    UserApp().run()
