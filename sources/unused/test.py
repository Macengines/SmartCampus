from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from circleimg import CircleImage  # Assuming you saved the above as circle_image.py

class TestApp(App):
    def build(self):
        root = BoxLayout()
        # Create CircleImage widget with custom source and size
        circle_img = CircleImage(size=[150, 150],pos_hint = {"center_y": .5, "center_x": .5})
        root.add_widget(circle_img)
        return root

if __name__ == '__main__':
    TestApp().run()
