from queue import Queue

from client.file import File


class Client:
    def __init__(self, id: int, files: list[File]) -> None:
        self.id = id
        self.pending: Queue[File] = Queue()
        self.in_progress: list[File] = []
        self.wait_time: float = 0

        for file in files:
            self.pending.put(file)

    def update_time(self, dt: float):
        self.wait_time += dt
