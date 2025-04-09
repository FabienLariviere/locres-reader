from io import BytesIO
from pathlib import Path
from typing import Iterator


class LocresFile:
    def __init__(self, location):
        self._location = Path(location)
        self._data = []

    def unpack(self) -> list[str]:
        with open(self._location, "rb") as f:
            data = f.read()
            stream = BytesIO(data)

        magic = int.from_bytes(stream.read(4), "little")
        if magic != 0x7574140E:
            raise Exception("Unsupported format!")

        stream.seek(0x10)

        end_bytes = int.from_bytes(stream.read(1), "little") > 1
        str_offset = int.from_bytes(stream.read(4), "little")

        stream.seek(str_offset)
        str_nums = int.from_bytes(stream.read(4), "little")
        strings = []

        for _ in range(str_nums):
            str_len = int.from_bytes(stream.read(4), "little", signed=True)

            string = ""

            if str_len > 0:
                string = stream.read(str_len).decode("ascii", errors="replace")
            elif str_len < 0:
                string = stream.read(str_len * -2).decode("utf-16le", errors="replace")

            strings.append(string.rstrip("\x00"))
            if end_bytes:
                stream.seek(4, 1)

        self._data = strings

    def dump(self):
        if not self._data:
            raise ValueError("Empty data")
        
        filename = Path(self._location.parent, f"{self._location.name}.txt")
        with open(filename, 'w') as file:
            file.writelines(map(lambda t: t+'\n', self._data))
        print(filename.absolute())


    def __iter__(self) -> Iterator[str]:
        return self._data