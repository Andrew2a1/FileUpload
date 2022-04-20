import threading
from typing import Optional

from client.client import Client
from client.file import File


class FolderObserver:
    def update_progress(self, progress: float):
        pass

    def update_upload_started(self, client: Client):
        pass

    def update_upload_finished(self, client: Client, file: File):
        pass


class Folder:
    def __init__(self):
        self.folder_thread: Optional[threading.Thread] = None
        self.exit_flag = threading.Event()
        self.observers: list[FolderObserver] = []
        self.upload_speed: float = 0

        self.total_files = 0
        self.total_data = 0

    def is_waiting(self) -> bool:
        return self.folder_thread is None or not self.folder_thread.is_alive()

    def set_upload_speed(self, upload_speed: float):
        self.upload_speed = upload_speed

    def attach_observer(self, observer: FolderObserver):
        self.observers.append(observer)

    def send_file(self, file: File, client: Client):
        if not self.is_waiting():
            raise Exception("Cannot send file when sending other file was not finished")
        self.folder_thread = threading.Thread(
            target=self.send_file_thread, args=[file, client]
        )
        self.folder_thread.start()

    def send_file_thread(self, file: File, client: Client):
        self.notify_upload_started(client)
        while not file.upload_finished():
            self.exit_flag.wait(0.05)
            if self.exit_flag.is_set():
                return

            send = file.upload_part(self.upload_speed)
            self.total_data += send
            self.notify_progress(file.upload_progress())

        self.total_files += 1
        self.notify_finished(client, file)

    def notify_upload_started(self, client: Client):
        for observer in self.observers:
            observer.update_upload_started(client)

    def notify_progress(self, progress: float):
        for observer in self.observers:
            observer.update_progress(progress)

    def notify_finished(self, client: Client, file: File):
        for observer in self.observers:
            observer.update_upload_finished(client, file)
