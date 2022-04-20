import math

import attr


def sizeof_fmt(num: float, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"


@attr.s(auto_attribs=True)
class File:
    size: int
    already_send: int = 0

    def __str__(self) -> str:
        return sizeof_fmt(self.size)

    def upload_part(self, dt: float):
        send = dt * max(1, math.log(self.size))
        self.already_send = int(min(self.size, self.already_send + send))

    def upload_progress(self) -> float:
        return self.already_send / self.size

    def upload_finished(self) -> bool:
        return self.already_send == self.size
