from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
import pyrebase

Window.size = (360, 640)

# Firebase Configuration
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

# Load the KV file
Builder.load_file("kv/datauser.kv")


class MyScreenManager(ScreenManager):
    pass


class UserItem(BoxLayout):
    user_id = StringProperty()
    name = StringProperty()
    email = StringProperty()

    def __init__(self, user_id, name, email, **kwargs):
        super(UserItem, self).__init__(**kwargs)
        self.user_id = user_id
        self.name = name
        self.email = email

    def delete_user(self):
        """Delete the user from Firebase."""
        db.child("users").child(self.user_id).remove()
        # Mendapatkan referensi ke UserList screen
        app = App.get_running_app()
        user_list_screen = app.root.get_screen("datauser")
        user_list_screen.update_user_list()

    def edit_user(self):
        """Navigate to the edit user screen."""
        app = App.get_running_app()
        edit_screen = app.root.get_screen("edit_user")
        edit_screen.load_user_data(self.user_id, self.name, self.email)
        app.root.current = "edit_user"
        


class UserList(Screen):
    def on_pre_enter(self):
        self.update_user_list()

    def update_user_list(self):
        self.ids.user_layout.clear_widgets()
        users = db.child("users").get().val()
        if users:
            for user_id, user_data in users.items():
                user_box = UserItem(user_id=user_id, name=user_data["name"], email=user_data["email"])
                self.ids.user_layout.add_widget(user_box)


class EditUserScreen(Screen):
    user_id = StringProperty()

    def load_user_data(self, user_id, name, email):
        self.user_id = user_id
        self.ids.name_input.text = name
        self.ids.email_input.text = email

    def save_user(self):
        name = self.ids.name_input.text
        email = self.ids.email_input.text
        db.child("users").child(self.user_id).update({"name": name, "email": email})
        App.get_running_app().root.current = "datauser"


class UserApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    UserApp().run()
