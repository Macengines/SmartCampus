from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
import requests

KV = '''
Screen:
    MDRaisedButton:
        text: "Upload File"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        on_release: app.open_file_manager()
'''

class AdminApp(MDApp):
    def build(self):
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_file
        )
        return Builder.load_string(KV)

    def open_file_manager(self):
        self.file_manager.show('/')

    def close_file_manager(self, *args):
        self.file_manager.close()

    def select_file(self, path):
        self.close_file_manager()
        self.upload_file(path)

    def upload_file(self, file_path):
        try:
            # Upload to Flask server
            url = 'http://127.0.0.1:5000/upload_vid'
            with open(file_path, 'rb') as file:
                response = requests.post(url, files={'file': file})
            
            if response.status_code == 200:
                self.show_dialog(f"Success: {response.json()['message']}")
            else:
                self.show_dialog("Failed to upload file!")
        except Exception as e:
            self.show_dialog(f"Error: {str(e)}")

    def show_dialog(self, message):
        dialog = MDDialog(
            title="File Upload",
            text=message,
            size_hint=(0.8, 1),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

if __name__ == "__main__":
    AdminApp().run()
