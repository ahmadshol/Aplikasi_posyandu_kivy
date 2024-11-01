from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior

Window.size = (360, 640)

# Load the KV file
Builder.load_file("kv/datapasien.kv")

class PatientItem(ButtonBehavior, BoxLayout):
    name = StringProperty()
    category = StringProperty()

    def __init__(self, name, category, **kwargs):
        super(PatientItem, self).__init__(**kwargs)
        self.name = name
        self.category = category

class PatientList(Screen):
    def __init__(self, **kwargs):
        super(PatientList, self).__init__(**kwargs)

        # Data pasien
        self.patients = [
            ("Rohmad Rafi N", "Lansia"),
            ("Musarof Morisorona", "Balita"),
            ("Anggit Hardianto", "Lansia"),
            ("Otto Santoso P", "Balita"),
            ("Syahrul Ageng P", "Lansia"),
            ("Irfan Ramadhan", "Balita"),
            ("Taufiq Fadhly R", "Lansia"),
            ("Bagas Fitriandra", "Balita")
        ]

        # Initial patient list display
        self.update_patient_list("All")

    def update_patient_list(self, category):
        # Clear current patient list
        self.ids.patient_layout.clear_widgets()

        # Filter and display patients based on selected category
        for name, patient_category in self.patients:
            if category == "All" or patient_category == category:
                patient_box = PatientItem(name=name, category=patient_category)
                self.ids.patient_layout.add_widget(patient_box)

class PatientApp(App):
    def build(self):
        return PatientList()

if __name__ == '__main__':
    PatientApp().run()
