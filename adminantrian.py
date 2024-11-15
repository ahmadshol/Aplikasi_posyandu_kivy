from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import os
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


class MyScreenManager(ScreenManager):
    pass

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
            
class AdminAntrianApp(App):
    def build(self):
        kv_files = ['adminantrian.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return AdminAntrianScreen()
    
    def set_queue_count(count):
        ref = db.reference('queue')
        ref.update({'count': count})
    
if __name__ == '__main__':
    AdminAntrianApp().run()