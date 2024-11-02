from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (360, 640)

class ImunisasiApp(App):
    def build(self):
        kv_files = ['imunisasi.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return ImunisasiScreen()

class ImunisasiScreen(Screen):
    pass

class RiwayatImunScreen(Screen):
    pass

if __name__ == '__main__':
    ImunisasiApp().run()
