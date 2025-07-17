from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20
        )

        self.search_bar = MDTextField(
            hint_text="Type to search...",
            mode="rectangle"
        )

        layout.add_widget(self.search_bar)
        self.add_widget(layout)


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return MainScreen()


MyApp().run()
