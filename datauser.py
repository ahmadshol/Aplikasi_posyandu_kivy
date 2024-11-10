from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (360, 640)

# Load the KV file
Builder.load_file("kv/datauser.kv")

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

class UserApp(App):
    def build(self):
        return UserList()

if __name__ == '__main__':
    UserApp().run()
