import re
import requests
from bs4 import BeautifulSoup


def random_task(task) -> dict:
    """
    Парсит задание по ссылке типа
    https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select={task}&answers=on&varId=
    Возвращает словарь
    {"html": html_content, "id": task_id, "answer": task_answer}
    :param task: Номер задания в КИМ от 1 до 27
    :return: dict
    """
    select_id = hex(int("1" + "0" * (task - 1), 2))[2:]
    url = f"https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select={select_id}&answers=on&varId="
    response = requests.get(url)

    if response:
        soup = BeautifulSoup(response.text, "lxml")
        tag_td = soup.find("td", {"class": "topicview"})
        script_lines = tag_td.find("script").text.strip().split("\n")
        task_id = re.search(r"\d+", script_lines[0]).group(0)
        html_content = re.findall(r"""\(([^\[\]]+)\)""", script_lines[1].replace("(", "", 1).strip()[:-2])

        tag_table = soup.find("table", {"class": "varanswer"})
        answer_table = {}
        for i, row in enumerate(tag_table.findAll("tr")):
            if i == 0:
                continue
            for egeno, answer in zip(row.find_all("td", {"class": "egeno"}), row.find_all("td", {"class": "answer"})):
                answer_table[egeno.text[:-1]] = answer.text
        return {"html": html_content, "id": task_id, "answer": answer_table[str(task)]}

    raise Exception("Невозможно обратиться к сайту Полякова")


if __name__ == "__main__":
    # пример
    a = random_task(23)
    print(a["id"])
    print(a["answer"])
    print(a["html"])
