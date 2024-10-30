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

class QueueScreen(Screen):
    pass

class DataLansiaScreen(Screen):
    pass

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
        # Ambil token pengguna dari screen login atau home (tergantung alur aplikasi Anda)
        login_screen = self.manager.get_screen('page_two')
        if hasattr(login_screen, 'user'):
            user = login_screen.user
            id_token = user['idToken']  # Mendapatkan idToken dari pengguna yang login

            # Ambil referensi semua pengguna dari Firebase Realtime Database
            try:
                users_ref = db.child("users").get(token=id_token)

                # Clear previous widgets (untuk menghindari duplikasi)
                self.ids.accounts_box.clear_widgets()

                # Cek apakah ada data pengguna
                if users_ref.each():  # Jika ada data
                    for doc in users_ref.each():
                        user_data = doc.val()

                        # Membuat ClickableBox untuk setiap pengguna
                        clickable_box = ClickableBox(user_data=user_data)
                        clickable_box.orientation = 'horizontal'
                        clickable_box.spacing = 10
                        clickable_box.padding = 10
                        clickable_box.size_hint_y = None
                        clickable_box.height = 70

                        # Styling kotak yang bisa diklik
                        with clickable_box.canvas.before:
                            Color(rgba=(0.9, 0.9, 0.9, 1))
                            RoundedRectangle(size=clickable_box.size, pos=clickable_box.pos, radius=[10, 10, 10, 10])

                        # Tambahkan gambar avatar
                        image = Image(source='img/avatar.png', size_hint=(None, None), size=(50, 50))
                        clickable_box.add_widget(image)

                        # Membuat box layout untuk nama dan email
                        box = BoxLayout(orientation='vertical', spacing=5)

                        # Label nama dan email
                        name_label = Label(text=user_data.get('name', 'No Name'), font_size='18sp', bold=True, size_hint_y=None, height=30, color=(0, 0, 0, 1))
                        email_label = Label(text=user_data.get('email', 'No Email'), font_size='14sp', size_hint_y=None, height=30, color=(0, 0, 0, 1))

                        # Tambahkan label ke dalam box layout
                        box.add_widget(name_label)
                        box.add_widget(email_label)

                        # Tambahkan box ke clickable_box
                        clickable_box.add_widget(box)

                        # Tambahkan clickable_box ke accounts_box layout
                        self.ids.accounts_box.add_widget(clickable_box)
                else:
                    print("No users found.")

            except Exception as e:
                print(f"Error fetching users: {e}")
        else:
            print("No user is logged in.")


class MyApp(App):
    def build(self):
        # Load all kv files
        kv_files = ['main.kv', 'home.kv', 'login.kv', 'registrasi.kv', 'account.kv', 'admin.kv','antrian.kv','datalansia.kv']
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return MyScreenManager()

    def login(self, email, password):
        try:
            # Login dengan Firebase Authentication menggunakan email dan password
            user = auth.sign_in_with_email_and_password(email, password)

            # Simpan informasi pengguna di screen login
            login_screen = self.root.get_screen('page_two')  # Pastikan login_screen diambil dari screen login
            login_screen.user = user  # Simpan user di screen login

            # Ambil token pengguna
            id_token = user['idToken']

            # Gunakan token ini untuk mengambil data dari Realtime Database
            users_ref = db.child("users").child(user['localId']).get(token=id_token)
            
            # Cek apakah data pengguna ditemukan
            if users_ref.val():
                user_data = users_ref.val()
                role = user_data.get("role")

                # Validasi role pengguna dan beralih ke screen yang sesuai
                if role == "admin":
                    self.root.current = 'admin'  # Beralih ke halaman admin
                elif role == "user":
                    self.root.current = 'home'  # Beralih ke halaman user
                else:
                    popup = Popup(title='Error',
                                content=Label(text='Role not found'),
                                size_hint=(None, None), size=(400, 200))
                    popup.open()
            else:
                popup = Popup(title='Error',
                            content=Label(text='User data not found'),
                            size_hint=(None, None), size=(400, 200))
                popup.open()

        except Exception as e:
            popup = Popup(title='Login Error',
                        content=Label(text=str(e)),
                        size_hint=(None, None), size=(400, 200))
            popup.open()


    def register(self, name, email, password, role):
        try:
            # Registrasi dengan Firebase Authentication
            user = auth.create_user_with_email_and_password(email, password)

            # Simpan informasi pengguna di screen registrasi
            registrasi_screen = self.root.get_screen('registrasi')
            registrasi_screen.user = user  # Simpan user di screen registrasi

            # Dapatkan token pengguna
            id_token = user['idToken']

            # Simpan data pengguna ke Realtime Database
            db.child("users").child(user['localId']).set({
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }, token=id_token)

            popup = Popup(title='Registration Successful',
                        content=Label(text=f'Registration successful for {role}'),
                        size_hint=(None, None), size=(400, 200))
            popup.open()
        except Exception as e:
            popup = Popup(title='Registration Failed',
                        content=Label(text=str(e)),
                        size_hint=(None, None), size=(400, 200))
            popup.open()


if __name__ == '__main__':
    MyApp().run()
