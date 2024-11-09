from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (360, 640)

class DatabalitaApp(App):
    def build(self):
        kv_files = ['databalita.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DatabalitaScreen()

class DatabalitaScreen(Screen):
    def load_data(self):
        app = App.get_running_app()
        data_balita = app.db.child("data_balita").get()

        if data_balita.each():
            # Ambil data terakhir
            last_data = data_balita.each()[-1].val()

            # Setel data pada label di DataLansiaScreen
            self.ids.labelTinggi.text = f"Tinggi Badan: {last_data['tinggi_badan']}"
            self.ids.labelBerat.text = f"Berat Badan: {last_data['berat_badan']}"
            self.ids.labelLingkarLengan.text = f"Lingkar Lengan Atas: {last_data['lingkar_lengan_atas']}"
            self.ids.labelLingkarKepala.text = f"Lingkar Kepala: {last_data['lingkar_kepala']}"
            self.ids.labelRiwayat.text = f"Riwayat Penyakit: {last_data['riwayat_penyakit']}"

if __name__ == '__main__':
    DatabalitaApp().run()
