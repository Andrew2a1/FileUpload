from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

from client.client import Client

Builder.load_file("./widgets/kv/client_entry.kv")


class ClientEntry(GridLayout):
    def __init__(self, client: Client, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.update()

    def update(self):
        self.ids.client_id.text = str(self.client.id)
        self.update_files()
        self.update_time()

    def update_files(self):
        self.ids.files.text = ", ".join(
            str(file) for file in self.client.pending + self.client.in_progress
        )

    def update_time(self):
        self.ids.wait_time.text = "{:.2f}s".format(self.client.wait_time)
