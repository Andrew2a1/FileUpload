import threading

from client.file import File


class Client:
    def __init__(self, id: int, files: list[File]) -> None:
        self.id = id
        self.pending: list[File] = files
        self.in_progress: list[File] = []
        self.files_lock = threading.Lock()
        self.wait_time: float = 0

    def finished(self) -> bool:
        self.files_lock.acquire()
        finished = len(self.pending) == 0 and len(self.in_progress) == 0
        self.files_lock.release()
        return finished

    def pending_to_in_progress(self) -> File:
        self.files_lock.acquire()

        top = self.pending[0]
        del self.pending[0]
        self.in_progress.append(top)

        self.files_lock.release()
        return top

    def get_top_pending_size(self) -> int:
        self.files_lock.acquire()
        size = self.pending[0].size
        self.files_lock.release()
        return size

    def get_pending_count(self) -> int:
        self.files_lock.acquire()
        size = len(self.pending)
        self.files_lock.release()
        return size

    def remove_in_progress(self, file: File):
        self.files_lock.acquire()
        self.in_progress.remove(file)
        self.files_lock.release()

    def update_time(self, dt: float):
        self.wait_time += dt
