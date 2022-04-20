from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from widgets.client_entry import ClientEntry

Builder.load_file("./widgets/kv/history.kv")


class History(FloatLayout):
    layout = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_entries: list[ClientEntry] = []

    def update_clients(self, clients):
        self.remove_entries()
        for client in clients:
            entry = ClientEntry(client)
            self.layout.add_widget(entry)
            self.client_entries.append(entry)

    def update_clients_times(self):
        for entry in self.client_entries:
            entry.update_time()

    def update_clients_files(self):
        for entry in self.client_entries:
            entry.update_files()

    def remove_entries(self):
        for entry in self.client_entries:
            self.layout.remove_widget(entry)
        self.client_entries = []
