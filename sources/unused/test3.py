from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
import requests
import os

KV = """
BoxLayout:
    orientation: 'vertical'
    RecycleView:
        id: file_list
        viewclass: 'MDFlatButton'
        RecycleBoxLayout:
            orientation: 'vertical'
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
"""

class FileDownloaderApp(MDApp):
    def build(self):
        self.root = Builder.load_string(KV)
        self.load_files()
        return self.root

    def load_files(self):
        response = requests.get("http://localhost:5000/files")
        if response.status_code == 200:
            files = response.json()
            data = []
            for file in files:
                data.append({
                    'text': f"{file['name']} ({file['size']} KB)",
                    'on_release': lambda url=file['url']: self.download_file(url)
                })
            self.root.ids.file_list.data = data

    def download_file(self, url):
        local_path = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(url))
        with requests.get(f"http://localhost/{url}", stream=True) as r:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File downloaded to {local_path}")

FileDownloaderApp().run()
