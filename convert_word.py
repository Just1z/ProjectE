def convert(origin, destination):
    """
    В переменных origin и destination необходимо указывать абсолютные пути к файлам.
    :param origin: путь к файлу .doc; str
    :param destination: путь к файлу .docx; str
    :return: None
    """
    import win32com.client
    import os

    if not origin.endswith(".doc"):
        raise OSError("Конвертируемый файл не имеет расширение .doc")
    if not destination.endswith(".docx"):
        raise OSError("Файл для сохранения не имеет расширение .docx")

    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(os.path.abspath(origin))
    doc.SaveAs(destination, 16)
    doc.Close()
    word.Quit()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("origin", type=str)
    parser.add_argument("destination", type=str)

    args = parser.parse_args()
    convert(args.origin, args.destination)
