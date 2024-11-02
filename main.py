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
import pyrebase

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

class HomeApp(Screen):
    pass

class LoginSecondScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class RegistrationScreen(Screen):
    pass

class AdminScreen(Screen):
    pass

class DataLansiaScreen(Screen):
    pass

class DaftarScreen(Screen):
    pass

class ImunisasiScreen(Screen):
    pass

class RiwayatImunScreen(Screen):
    pass

class DatabalitaScreen(Screen):
    pass 

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

class AccountScreen(Screen):
    def on_pre_enter(self):
        login_screen = self.manager.get_screen('page_two')
        if hasattr(login_screen, 'user'):
            user = login_screen.user
            id_token = user['idToken']
            try:
                users_ref = db.child("users").get(token=id_token)
                self.ids.accounts_box.clear_widgets()
                if users_ref.each():
                    for doc in users_ref.each():
                        user_data = doc.val()
                        clickable_box = ClickableBox(user_data=user_data)
                        clickable_box.orientation = 'horizontal'
                        clickable_box.spacing = 10
                        clickable_box.padding = 10
                        clickable_box.size_hint_y = None
                        clickable_box.height = 70
                        with clickable_box.canvas.before:
                            Color(rgba=(0.9, 0.9, 0.9, 1))
                            RoundedRectangle(size=clickable_box.size, pos=clickable_box.pos, radius=[10, 10, 10, 10])

                        image = Image(source='img/avatar.png', size_hint=(None, None), size=(50, 50))
                        clickable_box.add_widget(image)

                        box = BoxLayout(orientation='vertical', spacing=5)
                        name_label = Label(text=user_data.get('name', 'No Name'), font_size='18sp', bold=True, size_hint_y=None, height=30, color=(0, 0, 0, 1))
                        email_label = Label(text=user_data.get('email', 'No Email'), font_size='14sp', size_hint_y=None, height=30, color=(0, 0, 0, 1))
                        box.add_widget(name_label)
                        box.add_widget(email_label)
                        clickable_box.add_widget(box)
                        self.ids.accounts_box.add_widget(clickable_box)
                else:
                    print("No users found.")
            except Exception as e:
                print(f"Error fetching users: {e}")
        else:
            print("No user is logged in.")

class MyApp(App):
    def build(self):
        kv_files = ['main.kv', 'home.kv', 'login.kv', 'registrasi.kv', 'account.kv', 'admin.kv','antrian.kv','datalansia.kv','pendaftaran.kv','datapasien.kv','datauser.kv','imunisasi.kv','databalita.kv','adminantrian.kv']
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return MyScreenManager()

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
            
if __name__ == '__main__':
    MyApp().run()
