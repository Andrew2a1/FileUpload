from client.file import File


class Client:
    def __init__(self, id: int, files: list[File]) -> None:
        self.id = id
        self.pending: list[File] = list(sorted(files, key=lambda k: k.size))
        self.in_progress: list[File] = []
        self.wait_time: float = 0

    def has_pending_files(self) -> bool:
        return len(self.pending) > 0

    def has_in_progress_files(self) -> bool:
        return len(self.in_progress) > 0

    def finished(self) -> bool:
        return not self.has_pending_files() and not self.has_in_progress_files()

    def pending_to_in_progress(self) -> File:
        first_file = self.pending[0]
        self.in_progress.append(first_file)
        self.pending = self.pending[1:]
        return first_file

    def get_top_pending_size(self) -> int:
        if len(self.pending) > 0:
            return self.pending[0].size
        return 0

    def remove_in_progress(self, file: File):
        self.in_progress.remove(file)

    def update_time(self, dt: float):
        self.wait_time += dt
