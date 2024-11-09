from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
import os
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (360, 640)

class DataLansiaScreen(Screen):
    def load_data(self):
        app = App.get_running_app()
        data_lansia = app.db.child("data_lansia").get()

        if data_lansia.each():
            # Ambil data terakhir
            last_data = data_lansia.each()[-1].val()

            # Setel data pada label di DataLansiaScreen
            self.ids.labelTinggi.text = f"Tinggi Badan: {last_data['tinggi_badan']}"
            self.ids.labelBerat.text = f"Berat Badan: {last_data['berat_badan']}"
            self.ids.labelTekanan.text = f"Tekanan Darah: {last_data['tekanan_darah']}"
            self.ids.labelGula.text = f"Kadar Gula Darah: {last_data['gula_darah']}"
            self.ids.labelKolestrol.text = f"Kolestrol: {last_data['kolestrol']}"
            self.ids.labelRiwayat.text = f"Riwayat Penyakit: {last_data['riwayat_penyakit']}"
            
class DataLansiaApp(App):
    def build(self):
        kv_files = ['datalansia.kv']  # List more .kv files as needed
        for kv_file in kv_files:
            kv_file_path = os.path.join(os.path.dirname(__file__), 'kv', kv_file)
            Builder.load_file(kv_file_path)
        return DataLansiaScreen()



if __name__ == '__main__':
    DataLansiaApp().run()
