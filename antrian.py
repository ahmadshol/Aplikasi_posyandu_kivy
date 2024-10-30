from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
import os

Window.size = (360,640)

class QueueApp(App):
    def build(self):
        kv_file_path = os.path.join(os.path.dirname(__file__), 'kv','main.kv')
        Builder.load_file(kv_file_path)
        return QueueLayout()

class QueueLayout(BoxLayout):
    pass

if __name__ == '__main__':
    QueueApp().run()
