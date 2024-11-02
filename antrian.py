from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from main import firebase, db
import os

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

if __name__ == '__main__':
    QueueApp().run()
