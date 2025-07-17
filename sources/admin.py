from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
import requests
import os

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
        self.file_manager.show(os.path.expanduser("~"))  # Default to user home

    def close_file_manager(self, *args):
        self.file_manager.close()

    def select_file(self, path):
        self.close_file_manager()
        self.upload_file(path)

    def upload_file(self, file_path):
        try:
            url = 'http://127.0.0.1:5000/api/upload_file'
            with open(file_path, 'rb') as file:
                response = requests.post(url, files={'file': file})
            
            if response.status_code == 200:
                self.show_dialog(f"✅ Success: {response.json()['message']}")
            else:
                self.show_dialog(f"❌ Upload failed: {response.text}")
        except Exception as e:
            self.show_dialog(f"⚠️ Error: {str(e)}")

    def show_dialog(self, message):
        if not hasattr(self, 'dialog'):
            self.dialog = MDDialog(title="Upload Status", text=message)
        else:
            self.dialog.text = message
        self.dialog.open()

if __name__ == '__main__':
    AdminApp().run()
