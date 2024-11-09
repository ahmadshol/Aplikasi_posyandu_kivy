from kivy.config import Config
import os
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image


# Set the window size
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

class HomeApp(Screen):
    data_list = ListProperty([])

    def on_pre_enter(self):
        # Ambil data dari Firebase dan perbarui RecycleView
        balita_data = App.get_running_app().firebase_db.child("balita").get()
        lansia_data = App.get_running_app().firebase_db.child("lansia").get()

        data_list = []
        if balita_data.each():
            for item in balita_data.each():
                data_list.append({
                    'nama': item.val().get('nama'),
                    'kategori': 'Balita',
                    'target_screen': 'databalita'
                })

        if lansia_data.each():
            for item in lansia_data.each():
                data_list.append({
                    'nama': item.val().get('nama'),
                    'kategori': 'Lansia',
                    'target_screen': 'datalansia'
                })

        self.data_list = data_list

class ClickableImage(ButtonBehavior, Image):
    pass

class ClickBox(BoxLayout):
    kategori = StringProperty('')  # Mendefinisikan atribut 'kategori'
    nama = StringProperty('') 

class UserApp(App):
    def build(self):
        # Ensure the path to the kv file is correct
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv','home.kv')
        Builder.load_file(kv_file_path)
        return HomeApp()

if __name__ == '__main__':
    UserApp().run()
