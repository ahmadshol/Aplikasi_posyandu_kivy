from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.size = (360, 640)

class PatientList(BoxLayout):
    def __init__(self, **kwargs):
        super(PatientList, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Define patient data
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
        
        # Create a Spinner for category selection
        self.category_spinner = Spinner(
            text="All",
            values=["All", "Lansia", "Balita"],
            size_hint=(1, None),
            height=50
        )
        self.category_spinner.bind(text=self.update_patient_list)
        self.add_widget(self.category_spinner)
        
        # ScrollView and patient layout
        self.scroll_view = ScrollView()
        self.patient_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=[0, 10])
        self.patient_layout.bind(minimum_height=self.patient_layout.setter('height'))
        self.scroll_view.add_widget(self.patient_layout)
        
        # Add the ScrollView to the main layout
        self.add_widget(self.scroll_view)
        
        # Display initial patient list
        self.update_patient_list(None, "All")  # Updated call with two arguments

    def update_patient_list(self, spinner, category):
        # Clear the current patient list
        self.patient_layout.clear_widgets()
        
        # Filter and display patients based on selected category
        for name, patient_category in self.patients:
            if category == "All" or patient_category == category:
                patient_box = BoxLayout(
                    orientation='horizontal', size_hint_y=None, height=80,
                    padding=[5, 5, 5, 5], spacing=10
                )
                with patient_box.canvas.before:
                    Color(1, 1, 1, 1)  # White background for each card
                    rect = RoundedRectangle(size=patient_box.size, pos=patient_box.pos, radius=[10])
                    patient_box.bind(pos=lambda instance, value, rect=rect: self.update_rect(instance, rect),
                                     size=lambda instance, value, rect=rect: self.update_rect(instance, rect))

                # Add patient details
                patient_box.add_widget(Image(source='avatar.png', size_hint_x=None, width=50))
                details_layout = BoxLayout(orientation='vertical')
                details_layout.add_widget(Label(text=name, font_size=16, color=(0, 0, 0, 1), bold=True))  # Black text color
                details_layout.add_widget(Label(text=patient_category, font_size=16, color=(0, 0, 0, 1)))  # Black text color
                patient_box.add_widget(details_layout)
                self.patient_layout.add_widget(patient_box)

    def update_rect(self, instance, rect):
        rect.pos = instance.pos
        rect.size = instance.size

class PatientApp(App):
    def build(self):
        return PatientList()

if __name__ == '__main__':
    PatientApp().run()
