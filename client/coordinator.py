from typing import Optional
from client.client import Client
from client.folder import Folder

import threading

class Coordinator:
    def __init__(self):
        self.coordinator_thread: Optional[threading.Thread] = None
        self.folder_free = threading.Condition()

        self.folders: list[Folder] = [Folder(self.folder_free) for _ in range(5)]
        self.clients: list[Client] = []

    def coordinate(self):
        if self.coordinator_thread == None or self.coordinator_thread.is_alive():
            return

        self.coordinator_thread = threading.Thread(target=self.__main_loop)
        self.coordinator_thread.run()

    def __main_loop(self):
        while len(self.clients) > 0:
            if not any(folder.finished.is_set() for folder in self.folders):
                self.folder_free.wait()

            

        
