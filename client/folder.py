import threading
from typing import Optional

from client.client import Client
from client.file import File


class FolderObserver:
    def notify(self, progress: int):
        pass


class Folder:
    def __init__(self, folder_free: threading.Event):
        self.current_client: Optional[Client] = None
        self.current_file: Optional[File] = None
        self.observers: list[FolderObserver] = []

        self.folder_free = folder_free
        self.finished = threading.Event()
        self.finished.set()

    def attach_observer(self, observer: FolderObserver):
        self.observers.append(observer)

    def fire_update(self):
        updater = threading.Timer(0.05, self.update, args=[0.05])
        updater.start()

    def set_client(self, client: Client):
        self.finished.clear()
        self.current_client = client
        self.current_file = client.pending_to_in_progress()
        self.fire_update()

    def update(self, dt: float):
        if self.current_client and self.current_file:
            self.current_file.upload_part(dt)
            self.notify_all(
                self.current_file.already_send / self.current_file.size * 100
            )
            if self.current_file.upload_finished():
                self.current_client.remove_in_progress(self.current_file)
                self.finished.set()
                self.folder_free.set()
            else:
                self.fire_update()

    def notify_all(self, progress: int):
        for observer in self.observers:
            observer.notify(progress)
