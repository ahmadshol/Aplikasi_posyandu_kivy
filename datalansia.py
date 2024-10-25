from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os

Window.size = (360, 640)

class DataLansiaApp(App):
    def build(self):
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv','main.kv')
        Builder.load_file(kv_file_path)
        return DataLansiaLayout()

class DataLansiaLayout(BoxLayout):
    pass

if __name__ == '__main__':
    DataLansiaApp().run()
