from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import pyrebase

# Konfigurasi Firebase
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

# Memuat file KV
Builder.load_file("kv/datapasien.kv")


class MyScreenManager(ScreenManager):
    pass


class PatientItem(BoxLayout):
    name = StringProperty()
    category = StringProperty()
    
    def edit_data(self):
        # Panggil layar edit dan kirimkan data yang akan diubah
        app = App.get_running_app()
        app.root.current = 'edit_patient'
        app.root.get_screen('edit_patient').load_patient_data(self.name, self.category)

    def delete_data(self):
        # Hapus data dari database berdasarkan nama
        if self.category == "Balita":
            # Mengambil data balita berdasarkan nama dan menghapusnya
            balita_data = db.child("data_balita").order_by_child("nama").equal_to(self.name).get()
            if balita_data.each():
                for balita in balita_data.each():
                    db.child("data_balita").child(balita.key()).remove()
                    print(f"{self.name} berhasil dihapus dari balita")
            else:
                print(f"Pasien dengan nama {self.name} tidak ditemukan di kategori Balita")
        elif self.category == "Lansia":
            # Mengambil data lansia berdasarkan nama dan menghapusnya
            lansia_data = db.child("data_lansia").order_by_child("nama").equal_to(self.name).get()
            if lansia_data.each():
                for lansia in lansia_data.each():
                    db.child("data_lansia").child(lansia.key()).remove()
                    print(f"{self.name} berhasil dihapus dari lansia")
            else:
                print(f"Pasien dengan nama {self.name} tidak ditemukan di kategori Lansia")



class PatientList(Screen):
    def __init__(self, **kwargs):
        super(PatientList, self).__init__(**kwargs)
        self.patients = []

    def on_pre_enter(self):
        # Memuat data pasien ketika memasuki layar
        self.load_patients_data("All")

    def load_patients_data(self, category_filter):
        # Menghapus pasien dari daftar
        self.patients.clear()
        
        # Menyimpan nama yang telah diambil untuk menghindari duplikasi
        seen_names = set()

        # Mengambil data pasien 'Balita'
        balita_data = db.child("data_balita").get()
        if balita_data.each():
            for balita in balita_data.each():
                name = balita.val().get("nama", "Unknown")
                if balita.val() and name not in seen_names:
                    self.patients.append((name, "Balita"))
                    seen_names.add(name)

        # Mengambil data pasien 'Lansia'
        lansia_data = db.child("data_lansia").get()
        if lansia_data.each():
            for lansia in lansia_data.each():
                name = lansia.val().get("nama", "Unknown")
                if lansia.val() and name not in seen_names:
                    self.patients.append((name, "Lansia"))
                    seen_names.add(name)

        # Memperbarui tampilan berdasarkan filter
        self.update_patient_list(category_filter)

    def update_patient_list(self, category_filter):
        # Membersihkan item sebelumnya di layout
        self.ids.patient_layout.clear_widgets()

        # Menambahkan item pasien yang difilter ke layout
        for name, category in self.patients:
            if category_filter == "All" or category == category_filter:
                patient_box = PatientItem(name=name, category=category)
                self.ids.patient_layout.add_widget(patient_box)


class EditPatientScreen(Screen):
    name = StringProperty()
    category = StringProperty("")

    def load_patient_data(self, name, category):
        self.current_name = name
        self.current_category = category
        # Mencari data pasien berdasarkan nama
        patient_data = None

        # Cari di tabel Balita
        balita_data = db.child("data_balita").order_by_child("nama").equal_to(name).get()
        if balita_data.each():
            patient_data = balita_data.each()[0].val()
            self.current_category = "Balita"  # Menandai kategori Balita
        else:
            # Jika tidak ditemukan di balita, cari di lansia
            lansia_data = db.child("data_lansia").order_by_child("nama").equal_to(name).get()
            if lansia_data.each():
                patient_data = lansia_data.each()[0].val()
                self.current_category = "Lansia"  # Menandai kategori Lansia
        
        if patient_data:
            self.ids.name_input.text = patient_data.get("nama", "")
            self.ids.category_input.text = self.current_category  # Menampilkan kategori yang ditemukan
        else:
            # Tangani kasus jika data pasien tidak ditemukan
            print(f"Data pasien dengan nama {name} tidak ditemukan.")
            self.ids.name_input.text = ""
            self.ids.category_input.text = ""

    def save_changes(self):
        # Ambil data baru dari input
        new_name = self.ids.name_input.text
        new_category = self.ids.category_input.text

        # Update data pasien di Firebase
        updated_data = {
            "nama": new_name,
            "kategori": new_category
        }

        # Memperbarui data pasien berdasarkan nama dan kategori yang ditemukan
        if self.current_category == "Balita":
            # Cari di tabel Balita
            balita_data = db.child("data_balita").order_by_child("nama").equal_to(self.current_name).get()
            if balita_data.each():
                db.child("data_balita").child(balita_data.each()[0].key()).update(updated_data)
                print(f"Data {new_name} berhasil diperbarui di Balita")
        elif self.current_category == "Lansia":
            # Cari di tabel Lansia
            lansia_data = db.child("data_lansia").order_by_child("nama").equal_to(self.current_name).get()
            if lansia_data.each():
                db.child("data_lansia").child(lansia_data.each()[0].key()).update(updated_data)
                print(f"Data {new_name} berhasil diperbarui di Lansia")

        # Kembali ke layar daftar pasien
        app = App.get_running_app()
        app.root.current = "pasien"



class PatientApp(App):
    def build(self):
        return PatientList()


if __name__ == '__main__':
    PatientApp().run()
