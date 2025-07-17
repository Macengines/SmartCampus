from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.properties import ColorProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior


Builder.load_string('''
<BackBox2>:
    canvas.before:
        Color:
            rgba: self.bcolor
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: self.radius
''')
class BackBox2(BoxLayout, ButtonBehavior):
    bcolor = ColorProperty([1,1,1,0])
    radius = ListProperty([.5])
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
 
