from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MySpinnerApp(App):
    def build(self):
        layout = BoxLayout(orientation ="vertical")
        spinner=Spinner(text='select an option',
                        values=['option1','option2',"option3"]
                        )

        self.label = Label(text='')
        spinner.bind(text=self.label)
        layout.add_widget(spinner)
        layout.add_widget(self.label)

        return layout
    
    def update_label(self, instance, value):
        self.label.text = value

if __name__ =="__main__":
    MySpinnerApp().run()