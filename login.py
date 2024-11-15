from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
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

Window.size = (360, 640)

class MyScreenManager(ScreenManager):
    pass

class LoginScreen(Screen):
    pass

class LoginSecondScreen(Screen):
    def login(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                app = App.get_running_app()
                app.user_id = user['localId']
                app.id_token = user['idToken']

                # Ambil data pengguna
                users_ref = db.child("users").child(app.user_id).get(token=app.id_token)
                if users_ref.val():
                    user_data = users_ref.val()
                    name = user_data.get("name", "Nama tidak ada")
                    email = user_data.get("email", "Email tidak ada")
                    
                    # Tampilkan data pengguna setelah sedikit penundaan untuk memastikan layar profil siap
                    Clock.schedule_once(lambda dt: self.update_profil_screen(name, email))
                    
                    # Navigasi berdasarkan role
                    role = user_data.get("role")
                    if role == "admin":
                        self.root.current = 'admin'
                    elif role == "user":
                        self.root.current = 'profil'
                    else:
                        print("Role tidak ditemukan")
                else:
                    print("Data pengguna tidak ditemukan.")
            else:
                raise Exception("Login gagal, data pengguna tidak ditemukan.")
        except Exception as e:
            print("Login Error:", e)

    def update_profil_screen(self, name, email):
        profil_screen = self.root.get_screen('profil')
        profil_screen.display_name(name)
        profil_screen.display_email(email)

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

class HealthApp(App):
    def build(self):
        kv_files = ['login.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        
        client_id = open("json/client_id.txt")
        client_secret = open("json/client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
        
        # Cek jika sudah login sebelumnya
        self.check_if_logged_in()

        return MyScreenManager()

    def check_if_logged_in(self):
        """Cek apakah ada pengguna yang sudah login pada saat aplikasi dimulai."""
        user = auth.current_user
        if user:
            print(f"Pengguna sudah login: {user['email']}")
            self.after_login(user['email'], user['email'], None)
        else:
            print("Tidak ada pengguna yang login.")

    def after_login(self, name, email, photo_uri):
        account_screen = self.root.get_screen('page_one')  # Mendapatkan instance AccountScreen
        account_screen.ids.label.text = f"logged as {name}"
        self.root.transition.direction = "left"
        self.root.current = "home"
        
    def error_listener(self):
        print("Login failed!!!")
    
    def loginn(self):
        login_google()
        
    def logout(self):
        logout_google(self.after_logout())
        
    def after_logout(self):
        self.root.ids.label.text = ""
        self.root.ids.transition.direction = "right"
        self.root.current = "page_one"
        
    def login(self, email, password):
        try:
            # Proses login Firebase Authentication
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                login_screen = self.root.get_screen('page_two')
                login_screen.user = user
                id_token = user['idToken']
                users_ref = db.child("users").child(user['localId']).get(token=id_token)
                if users_ref.val():
                    user_data = users_ref.val()
                    name = user_data.get("name")
                    print("name:", name)
                    email = user_data.get("email")
                    print ("email:", email)
                    print("Data pengguna:", user_data)
                    role = user_data.get("role")
                    
                    if role == "admin":
                        self.root.current = 'admin'
                    elif role == "user":
                        self.root.current = 'home'
                    else:
                        Popup(title='Error', content=Label(text='Role not found'), size_hint=(None, None), size=(400, 200)).open()
                else:
                    Popup(title='Error', content=Label(text='User data not found'), size_hint=(None, None), size=(400, 200)).open()
            else:
                raise Exception("Login gagal, data pengguna tidak ditemukan.")
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
    HealthApp().run()
