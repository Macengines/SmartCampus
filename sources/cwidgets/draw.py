from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton


class DrawWidget(Widget):
    drawing_enabled = False  # Controls if drawing is active

    def on_touch_down(self, touch):
        if self.drawing_enabled:
            with self.canvas:
                Color(0.6, 0, 0.6, 1)  # Purple color
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=3)

    def on_touch_move(self, touch):
        if self.drawing_enabled and 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

    def clear_canvas(self):
        self.canvas.clear()


class DrawingApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation="vertical")

        self.draw_widget = DrawWidget()
        layout.add_widget(self.draw_widget)

        # Toggle button for pencil activation
        self.pencil_button = MDRaisedButton(text="Activate Pencil", pos_hint={"center_x": 0.5})
        self.pencil_button.bind(on_release=self.toggle_pencil)
        layout.add_widget(self.pencil_button)

        # Clear button
        clear_btn = MDRaisedButton(text="Clear", pos_hint={"center_x": 0.5})
        clear_btn.bind(on_release=lambda x: self.draw_widget.clear_canvas())
        layout.add_widget(clear_btn)

        return layout

    def toggle_pencil(self, instance):
        # Toggle drawing mode
        self.draw_widget.drawing_enabled = not self.draw_widget.drawing_enabled
        instance.text = "Deactivate Pencil" if self.draw_widget.drawing_enabled else "Activate Pencil"


if __name__ == '__main__':
    DrawingApp().run()
