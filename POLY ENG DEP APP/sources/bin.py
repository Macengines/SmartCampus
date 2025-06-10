from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.uix.box2 import BackBox2
from kivy.utils import rgba
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDTextButton
import textwrap
from kivy.uix.box import BackBox
from kivy.uix.textfields import FlatField
from kivy.properties import  ColorProperty
from kivy.uix.draw import DrawWidget
from kivy.uix.spinner2 import Spinner2
from kivy.uix.textinput import TextInput



KV = '''
MDScreen:
    id: main_screen
    BackBox:
        bcolor: app.color_bg_cream
        orientation: "vertical"
        spacing: 20
        BackBox:
            size_hint_y: .08
            bcolor: app.color_bg_white
            spacing: 10
            MDIconButton:
                size_hint_x: .1
                icon: "chevron-double-left"
                valign: "center"
                
            BackBox:
                size_hint_x: .5
                padding: 10
                FlatField:
                    hint_text: "Title"
            BackBox:
                size_hint_x: .4
                bcolor: app.color_dark_blue
                valign: "center"
                halign:"center"
                MDIconButton:
                    icon: "content-save-all"
                    size_hint_x: .15
                MDIconButton:
                    icon: "checkbox-multiple-outline"
                    size_hint_x: .15
                MDIconButton:
                    icon: "text-box-edit-outline"
                    size_hint_x: .15
                BackBox:
                    size_hint_x: .15
                    orientation: "vertical"
                    FloatLayout:
                        MDIconButton:
                            icon: "format-text"
                            size_hint_y: .9
                            pos_hint: {"center_y": 0.5, "center_x": .5}
                        MDIcon:
                            size_hint_y: .1
                            icon: "minus-thick"
                            pos_hint: {"center_y": 0.2, "center_x": .5}
                            theme_text_color: "Custom"
                            text_color: (1, 0, 0, 1)
                        
                    
                Spinner2:
                    text:"17"
                    values: ["16","17","18","19","20","21",]
                    pos_hint: {"center_y": 0.5}
                    size_hint_x: .15
                MDIconButton:
                    icon: "draw"
                    on_release: app.toggle_pencil()
                    size_hint_x: .15
                MDIconButton:
                    icon: "eraser"
                    on_release:app.clear()
                    size_hint_x: .15

                
        BackBox:
            size_hint_y: .92
            bcolor: app.color_bg_white
            orientation: "vertical"
            padding: 5
            BackBox:
                size_hint_y: .99
                TextInput:
                    id: note_field
                    hint_text: "Write your notes here..."
                    multiline: True
                    normal_color: (1, 1, 1, 1)  # White background
                    background_normal: ''  # Remove default background image
                    background_color: (1, 1, 1, 1)  # Keep the background white
                    line_color_normal: (1, 1, 1, 0)  # Remove line
                    line_color_focus: (1, 1, 1, 0)  # Remove line on focus
                    foreground_color: (0, 0, 0, 1)  # Set text color to black for visibility
                    cursor_color: (0, 0, 0, 1)  # Set cursor color to black for visibility
                    padding: [10, 10, 10, 10]  # Add padding to the text field
                    text_color: (0, 0, 0, 1)  # Set text color to black for visibility  
            DrawWidget:
                size_hint_y: .01
                id: draw_widget
'''

class MyApp(MDApp):
    def build(self):
        screen = Builder.load_string(KV)
        return screen
    def clear(self):
        # Corrected reference to the draw widget
        draw_widget = self.root.ids.draw_widget  
        draw_widget.clear_canvas()
    def toggle_pencil(self):
        # Toggle drawing mode
        draw_widget = self.root.ids.draw_widget
        draw_widget.drawing_enabled = not draw_widget.drawing_enabled
        draw_widget.text = "Deactivate Pencil" if draw_widget.drawing_enabled else "Activate Pencil"

    theme = "light"
    color_bg_cream = ColorProperty(rgba("#E9E3E3"))
    color_bg_white = ColorProperty(rgba("#FFFFFF"))
    color_bg_black = ColorProperty(rgba("#000000"))
    color_light_blue = ColorProperty(rgba("#00B0F0"))
    color_light_blue2 = ColorProperty(rgba("#C1E5F5"))
    color_dark_blue = ColorProperty(rgba("#0070C0"))
    color_bg_grey = ColorProperty(rgba("#EFEFEF"))
    color_bg_dovegrey = ColorProperty(rgba("#3D5F62"))
    color_text_light = ColorProperty(rgba("#7F7F7F"))
    color_stars_yellow = ColorProperty(rgba("#FFFF00"))
    color_primary_bg = ColorProperty(rgba("#FFFFFF"))
    color_bg_orange = ColorProperty(rgba("#FFFFFF"))
MyApp().run()
