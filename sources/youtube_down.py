from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
import requests
from cwidgets.box import BackBox

KV = '''
Screen:
    id:screen
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    BackBox:
        bcolor: (rgba("#00B0F0"))
        radius: [15]
        pos_hint:{"center_y" :.5, "center_x": .5}
        Image:
            source:".venv/assets/imgs/MACTECH LIGHT(1).PNG"
            
'''

class AdminApp(MDApp):
    def build(self):
        
        return Builder.load_string(KV)

if __name__ == "__main__":
    AdminApp().run()
