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

class PatientItem(BoxLayout):
    name = StringProperty("")
    unique_id = StringProperty("")  # Mengganti balita_id menjadi unique_id
    category = StringProperty("Balita")  # Default kategori untuk balita
    
class DaftarbalitaScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.load_balita_data, 0.5)  # Schedule to load data after entering the screen

    def load_balita_data(self, *args):
        self.ids.patient_layout.clear_widgets()  # Clear previous list items
        data_balita = db.child("data_balita").get()
        
        if data_balita.each():
            for balita in data_balita.each():
                name = balita.val().get("name", "Unknown")  # Retrieve name
                patient_id = balita.key()  # Unique ID for each record
                
                patient_item = PatientItem(name=name, unique_id=patient_id, category="Balita")
                self.ids.patient_layout.add_widget(patient_item)

    def go_to_imunisasi_screen(self, patient_id):
        # Set any required data for the ImunisasiScreen here
        self.manager.current = 'imunisasi'  # Navigate to Imunisasi screen

if __name__ == '__main__':
    ImunisasiApp().run()
