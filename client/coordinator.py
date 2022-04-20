import threading
from typing import Optional

from client.client import Client
from client.folder import Folder


class Coordinator:
    def __init__(self):
        self.coordinator_thread = threading.Thread(target=self.__main_loop)
        self.folder_free = threading.Event()
        self.clients_lock = threading.Lock()

        self.folders: list[Folder] = [Folder(self.folder_free) for _ in range(5)]
        self.clients: list[Client] = []

    def add_client(self, client: Client):
        self.clients_lock.acquire()
        self.clients.append(client)
        self.clients_lock.release()
        self.coordinate()

    def coordinate(self):
        if self.coordinator_thread.is_alive():
            return

        self.coordinator_thread = threading.Thread(target=self.__main_loop)
        self.coordinator_thread.run()

    def __main_loop(self):
        while self.client_count() > 0:
            self.clients_lock.acquire()
            self.clients = [client for client in self.clients if not client.finished()]
            winner = self.find_winner(self.clients)
            self.clients_lock.release()

            if not winner:
                break

            if not any(folder.finished.is_set() for folder in self.folders):
                self.folder_free.wait()

            self.folder_free.clear()

            for folder in self.folders:
                if folder.finished.is_set():
                    folder.set_client(winner)

    def client_count(self) -> int:
        self.clients_lock.acquire()
        count = len(self.clients)
        self.clients_lock.release()
        return count

    def find_winner(self, clients: list[Client]) -> Optional[Client]:
        clients_count = len(clients)
        scores = [
            (client, self.get_score(client, clients_count))
            for client in clients
            if client.get_pending_count() > 0
        ]

        if len(scores) == 0:
            return None
        return max(scores, key=lambda s: s[1])[0]

    def get_score(self, client: Client, clients_count: int) -> float:
        t = client.wait_time
        s = client.get_top_pending_size()
        c = clients_count
        return t / (c + 1) + c / (s + 1)
