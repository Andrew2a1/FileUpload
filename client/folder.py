import threading
from typing import Optional

from client.file import File


class FolderObserver:
    def notify(self, progress: int):
        pass


class Folder:
    def __init__(self):
        self.folder_thread: Optional[threading.Thread] = None
        self.exit_flag = threading.Event()
        self.upload_speed: float = 0
        self.progress: float = 0

    def is_waiting(self) -> bool:
        return self.folder_thread is None or not self.folder_thread.is_alive()

    def set_upload_speed(self, upload_speed: float):
        self.upload_speed = upload_speed

    def send_file(self, file: File):
        if not self.is_waiting():
            raise Exception("Cannot send file when sending other file was not finished")
        self.folder_thread = threading.Thread(target=self.send_file_thread, args=[file])
        self.folder_thread.start()

    def send_file_thread(self, file: File):
        while not file.upload_finished():
            self.exit_flag.wait(0.05)
            if self.exit_flag.is_set():
                break

            file.upload_part(self.upload_speed)
            self.progress = file.upload_progress()
