from kivy.uix.stencilview import StencilView
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder

Builder.load_string('''
<CircleImage>:
    size_hint: None, None
    size: root.size
    canvas.before:
        Ellipse:
            pos: self.pos
            size: self.size
    Image:
        source: ".venv/assets/imgs/images(1).png"
        pos: self.pos
        size: self.size
        allow_stretch: True
        keep_ratio: True
''')

class CircleImage(StencilView):
    #source =        # Image path property
    size = ListProperty([200, 200])    # Size property, default 200x200
