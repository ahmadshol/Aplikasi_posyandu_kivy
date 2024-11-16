from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
import os
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

Window.size = (360,640)

class QueueApp(App):
   def build(self):
        kv_files = ['antrian.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return QueueScreen()

class QueueScreen(Screen):
    def on_enter(self):
        # Menampilkan nomor antrian yang diambil
        user_id = self.get_current_user_id()
        if user_id:
            nomor_antrian = db.child("nomor_antrian").child(user_id).get(token=App.get_running_app().id_token).val() or []
            self.ids.taken_queue_label.text = "\n".join(nomor_antrian)
        else:
            self.ids.taken_queue_label.text = "ID Pengguna tidak tersedia."

    def get_current_user_id(self):
        # Mengambil user_id dari instance aplikasi
        app = App.get_running_app()
        return app.user_id if hasattr(app, 'user_id') else None

    def get_name(self):
        # Mendapatkan nama pengguna dari profil pengguna
        app = App.get_running_app()
        return app.name if hasattr(app, 'name') else "User Tanpa Nama"

    def get_queue(self):
        user_id = self.get_current_user_id()
        if not user_id:
            self.ids.queue_label.text = "Gagal mengambil antrian, ID Pengguna tidak tersedia."
            return

        nomor_antrian = db.child("nomor_antrian").child(user_id).get(token=App.get_running_app().id_token).val() or []

        if len(nomor_antrian) < 2:
            count = db.child("queue/count").get().val()
            if count and count > 0:
                queue_number = count
                db.child("queue").update({"count": count - 1})

                name = self.get_name()
                nomor_antrian.append(f"{name}: Antrian {queue_number}")

                try:
                    db.child("nomor_antrian").child(user_id).set(nomor_antrian, token=App.get_running_app().id_token)
                    self.ids.queue_label.text = f"Antrian Diambil, Nomor: {queue_number}"

                    # Update label di HomeApp
                    app = App.get_running_app()
                    home_screen = app.root.get_screen("home")  # Ganti "home" dengan nama layar HomeApp di ScreenManager
                    home_screen.update_queue_label(nomor_antrian)

                except Exception as e:
                    self.ids.queue_label.text = f"Gagal mengambil antrian: {e}"
            else:
                self.ids.queue_label.text = "Antrian Habis"
        else:
            self.ids.queue_label.text = "Anda sudah mengambil 2 antrian."

    def show_remaining_queue(self):
        # Menampilkan sisa antrian di admin
        remaining_count = db.child("queue/count").get().val()
        self.ids.remaining_queue_label.text = f"Sisa Antrian: {remaining_count}"
    
    def update_home_queue_label(self, nomor_antrian):
        home_screen = self.root.get_screen('home')
        home_screen.update_queue_label(nomor_antrian)

if __name__ == '__main__':
    QueueApp().run()
