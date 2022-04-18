from typing import Optional

from client.client import Client
from client.file import File

import threading


class FolderObserver:
    def notify(self, progress: int):
        pass


class Folder:
    def __init__(self, free_condition: threading.Condition):
        self.current_client: Optional[Client] = None
        self.current_file: Optional[File] = None
        self.observers: list[FolderObserver] = []
        self.free_condition = free_condition
        self.finished = threading.Event()
        self.finished.set()

    def attach_observer(self, observer: FolderObserver):
        self.observers.append(observer)

    def set_client(self, client: Client):
        self.finished.clear()
        self.current_client = client
        self.current_file = client.pending.get()
        client.in_progress.append(self.current_file)

    def update(self, dt: float):
        if self.current_client and self.current_file:
            self.current_file.upload_part(dt)
            if self.current_file.upload_finished():
                self.current_client.in_progress.remove(self.current_file)
                self.finished.set()
                self.free_condition.notify()
            self.notify_all(
                self.current_file.already_send / self.current_file.size * 100
            )

    def notify_all(self, progress: int):
        for observer in self.observers:
            observer.notify(progress)
