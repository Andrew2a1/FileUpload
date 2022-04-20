from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout

Builder.load_file("./widgets/kv/folder_widget.kv")

from client.client import Client
from client.file import File, sizeof_fmt
from client.folder import Folder, FolderObserver


class FolderWidget(FloatLayout, FolderObserver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folder = None

    def set_folder(self, folder: Folder):
        self.folder = folder

    def update_progress(self, progress: float):
        self.ids.progress.value = progress * 100
        self.ids.file_count.text = f"Files: {self.folder.total_files}"
        self.ids.file_size.text = f"Size: {sizeof_fmt(self.folder.total_data)}"

    def update_upload_finished(self, client: Client, file: File):
        self.ids.current_client.text = "Client: None"

    def update_upload_started(self, client: Client):
        self.ids.current_client.text = f"Client: {client.id}"
