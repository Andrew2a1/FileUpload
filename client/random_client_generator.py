import random

from client.client import Client
from client.file import File


def IdGenerator():
    num = 0
    while True:
        num += 1
        yield num


class RandomClientGenerator:
    id_generator = IdGenerator()

    @staticmethod
    def generate(max_files=6, max_size=1e9) -> Client:
        new_files = []
        for _ in range(random.randint(1, max_files)):
            new_files.append(File(random.randint(1, int(max_size))))

        new_files.sort()
        new_id = next(RandomClientGenerator.id_generator)
        return Client(new_id, new_files)
