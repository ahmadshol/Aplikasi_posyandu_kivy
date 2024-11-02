from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

Window.size = (360, 640)

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

class ClickableBox(ButtonBehavior, BoxLayout):
    def __init__(self, user_data, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data

    def on_press(self):
        # When clicked, navigate to the home page and pass user data
        app = App.get_running_app()
        app.root.current = 'home'
        # You can pass more user data here if needed, like user ID
        app.root.get_screen('home').ids.welcome_label.text = f"Welcome, {self.user_data.get('name')}"

class AccountScreen(Screen):
    def on_pre_enter(self):
        # Menggunakan idToken untuk autentikasi
        if hasattr(self.manager.get_screen('page_one'), 'user'):  # Pastikan ini adalah screen login
            user = self.manager.get_screen('page_one').user  # Ambil dari screen login
            id_token = user['idToken']

            # Ambil referensi pengguna dari Firebase Realtime Database
            users_ref = db.child("users").get(token=id_token)

            # Clear previous widgets
            self.ids.accounts_box.clear_widgets()  # Bersihkan tampilan sebelumnya

            # Cek apakah ada data yang diambil
            if users_ref.each():  # Cek apakah ada data
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
                    # Pastikan nilai default jika 'name' atau 'email' hilang
                    name_label = Label(text=user_data.get('name', 'No Name'), font_size='18sp', bold=True, size_hint_y=None, height=30, color=(0, 0, 0, 1))
                    email_label = Label(text=user_data.get('email', 'No Email'), font_size='14sp', size_hint_y=None, height=30, color=(0, 0, 0, 1))
                    box.add_widget(name_label)
                    box.add_widget(email_label)
                    clickable_box.add_widget(box)

                    self.ids.accounts_box.add_widget(clickable_box)
            else:
                print("No users found.")  # Debug statement jika tidak ada pengguna yang ditemukan
        else:
            print("User not found in login screen.") 

class HomeApp(Screen):
    pass

class LoginSecondScreen(Screen):
    pass

class AccountApp(App):
    def build(self):
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', 'account.kv')
        Builder.load_file(kv_file_path)

        sm = ScreenManager()
        sm.add_widget(AccountScreen(name='account'))
        sm.add_widget(HomeApp(name='home'))
        return sm

if __name__ == '__main__':
    AccountApp().run()
