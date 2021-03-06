from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout

from client.coordinator import Coordinator
from client.random_client_generator import RandomClientGenerator
from widgets.client_entry import ClientEntry  # NOQA
from widgets.controls import Controls  # NOQA
from widgets.folder_widget import FolderWidget  # NOQA
from widgets.folders import Folders  # NOQA
from widgets.history import History  # NOQA

Builder.load_file("./widgets/kv/file_upload_layout.kv")


class FileUploadLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.coordinator = Coordinator()

        self.__bind_controls()
        for folder_no in range(5):
            self.coordinator.attach_to_folder(
                folder_no, self.ids.folders.ids[f"folder_{folder_no}"]
            )
            self.ids.folders.ids[f"folder_{folder_no}"].set_folder(
                self.coordinator.folders[folder_no]
            )

        self.speed = 0
        self.auto_clock = None
        self.clock = Clock.schedule_interval(self.update, 0.05)

    def exit(self):
        self.coordinator.exit()

    def __bind_controls(self):
        controls = self.ids.controls.ids
        controls.reset.bind(on_press=lambda _: self.reset())
        controls.auto.bind(state=lambda _, state: self.toggle_clock(state))
        controls.add.bind(on_press=lambda _: self.add_random_client())
        controls.speed_slider.bind(value=lambda _, speed: self.update_speed(speed / 10))

    def add_random_client(self):
        self.coordinator.clients.append(RandomClientGenerator.generate())
        self.update_clients()

    def reset(self):
        self.coordinator.clients = []
        self.update_clients()

    def update_clients(self):
        self.ids.history.update_clients(self.coordinator.clients)

    def toggle_clock(self, state: str):
        if state == "down":
            self.auto_clock = Clock.schedule_interval(
                lambda _: self.add_random_client(), 2
            )
        else:
            self.auto_clock.cancel()

    def update(self, dt: float):
        for client in self.coordinator.clients:
            client.update_time(dt * self.speed)

        self.update_clients()
        self.coordinator.coordinate()

    def update_speed(self, new_speed: int):
        self.speed = new_speed
        self.coordinator.set_speed(new_speed)
