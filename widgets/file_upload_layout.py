from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder

from widgets.control_widget import ControlWidget
from widgets.clients_queue import ClientsQueue
from widgets.client import Client
from widgets.folders import Folders
from widgets.folder import Folder

Builder.load_file("./widgets/kv/file_upload_layout.kv")

class FileUploadLayout(FloatLayout):
    pass
