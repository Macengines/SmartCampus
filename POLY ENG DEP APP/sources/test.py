import os
import json
from kivy.lang import Builder
from kivymd.app import MDApp

KV = """
Screen:
    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "10dp"

        MDTextField:
            id: note_field
            hint_text: "Write your notes here..."
            multiline: True
            mode: "fill"

        MDRaisedButton:
            text: "Save"
            pos_hint: {"center_x": 0.5}
            on_release: app.save_note()
"""

class NotesApp(MDApp):
    FILE_PATH = "notes.json"  # File where notes are stored

    def build(self):
        screen = Builder.load_string(KV)
        self.load_note()
        return screen

    def save_note(self):
        """Saves the text to a JSON file."""
        note_text = self.root.ids.note_field.text.strip()
        data = {"note": note_text}  # Store text in JSON format

        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_note(self):
        """Loads saved text from JSON when the app starts."""
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    self.root.ids.note_field.text = data.get("note", "")
                except json.JSONDecodeError:
                    self.root.ids.note_field.text = ""

NotesApp().run()
