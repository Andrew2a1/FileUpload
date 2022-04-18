from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout

from client.random_client_generator import RandomClientGenerator
from widgets.client_entry import ClientEntry  # NOQA
from widgets.controls import Controls  # NOQA
from widgets.folder_widget import FolderWidget  # NOQA
from widgets.folders import Folders  # NOQA
from widgets.history import History  # NOQA

Builder.load_file("./widgets/kv/file_upload_layout.kv")

from client.client import Client


class FileUploadLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__bind_controls()
        self.clients: list[Client] = []
        self.speed = 0
        self.clock = Clock.schedule_interval(self.update, 0.05)
        self.auto_clock = None

    def update_clients(self):
        valid_clients = [
            client
            for client in self.clients
            if len(client.in_progress) > 0 and not client.pending.empty()
        ]
        self.clients = valid_clients
        self.ids.history.update_clients(valid_clients)

    def __bind_controls(self):
        controls = self.ids.controls.ids
        controls.reset.bind(on_press=lambda _: self.reset())
        controls.auto.bind(state=lambda _, state: self.toggle_clock(state))
        controls.add.bind(on_press=lambda _: self.add_random_client())
        controls.speed_slider.bind(value=lambda _, speed: self.update_speed(speed / 10))

    def add_random_client(self):
        self.clients.append(RandomClientGenerator.generate())
        self.update_clients()

    def toggle_clock(self, state: str):
        if state == "down":
            self.auto_clock = Clock.schedule_interval(
                lambda _: self.add_random_client(), 2
            )
        else:
            self.auto_clock.cancel()

    def reset(self):
        self.clients = []
        self.update_clients()

    def update(self, dt: float):
        for client in self.clients:
            client.update_time(dt * self.speed)
        self.ids.history.update_clients_times()

        winner = self.find_winner(self.clients)
        

    def find_winner(self, clients: list[Client]):
        if len(clients) == 0:
            return

        scores = [(client, self.get_score(client, len(clients))) for client in clients]
        return max(scores, key=lambda s: s[1])[0]

    def get_score(self, client: Client, clients_count: int):
        t = client.wait_time
        s = client.pending[0].size
        c = clients_count
        return t / (c + 1) + c / (s + 1)

    def update_speed(self, new_speed: int):
        self.speed = new_speed
