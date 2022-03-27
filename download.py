import py7zr
from io import BytesIO
from requests import get

unpack_to = "/kpolyakov/"
binary = get("https://kpolyakov.spb.ru/download/ege2022kp.7z").content
file_object = BytesIO(binary)

with py7zr.SevenZipFile(file_object, mode='r', password="kpolyakov.spb.ru") as archive:
    archive.extractall()
    # z.extractall(path=unpack_to)  # непонятно как работает path, поэтому запускать следует из директории, куда нужно распаковать

