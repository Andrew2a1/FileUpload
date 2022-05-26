from typing import Optional

from client.client import Client
from client.file import File
from client.folder import Folder, FolderObserver


class Coordinator(FolderObserver):
    def __init__(self):
        self.folders: list[Folder] = [Folder() for _ in range(5)]
        self.clients: list[Client] = []

        for folder in self.folders:
            folder.attach_observer(self)

    def attach_to_folder(self, folder_no: int, observer: FolderObserver):
        self.folders[folder_no].attach_observer(observer)

    def exit(self):
        for folder in self.folders:
            if not folder.is_waiting():
                folder.exit_flag.set()
                folder.folder_thread.join()

    def set_speed(self, speed: float):
        for folder in self.folders:
            folder.set_upload_speed(speed * 1e5)

    def coordinate(self):
        clients_with_files = [
            client for client in self.clients if client.has_pending_files()
        ]
        winner = self.find_winner(clients_with_files)

        if winner is None:
            return

        for folder in self.folders:
            if folder.is_waiting():
                file_to_upload = winner.pending_to_in_progress()
                folder.send_file(file_to_upload, winner)
                break

    def update_upload_finished(self, client: Client, file: File):
        client.remove_in_progress(file)
        if client.finished():
            self.clients.remove(client)

    def find_winner(self, clients: list[Client]) -> Optional[Client]:
        clients_count = len(clients)
        scores = [
            (client, self.get_score(client, clients_count))
            for client in clients
            if client.wait_time > 0
        ]

        if len(scores) == 0:
            return None
        return max(scores, key=lambda s: s[1])[0]

    def get_score(self, client: Client, clients_count: int) -> float:
        t = client.wait_time
        s = client.get_top_pending_size()
        c = clients_count
        return t / (c + 1) + c / (s/1e7 + 1)
