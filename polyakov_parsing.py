import re
import requests
from bs4 import BeautifulSoup
from base64 import b64encode


def collect_variant(id):
    url = f"https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&answers=on&varId={id}"
    response = requests.get(url)

    if response:
        tasks = []
        soup = BeautifulSoup(response.text, "lxml")
        tags = soup.find_all("td", {"class": "topicview"})
        for tag_td in tags:
            script_lines = tag_td.find("script").text.strip().split("\n")
            task_id = re.search(r"\d+", script_lines[0]).group(0)
            html_content = re.findall(r"""\(([^\[\]]+)\)""", script_lines[1].replace("(", "", 1).strip()[:-2])
            tasks.append(html_content)

        tag_table = soup.find("table", {"class": "varanswer"})
        answer_table = {}
        for i, row in enumerate(tag_table.findAll("tr")):
            if i == 0:
                continue
            for egeno, answer in zip(row.find_all("td", {"class": "egeno"}), row.find_all("td", {"class": "answer"})):
                if answer.text:
                    answer_table[egeno.text[:-1]] = answer.text
        return {"html": tasks, 'answer': answer_table}

    raise Exception("Невозможно обратиться к сайту Полякова")


def collect_task(url):
    response = requests.get(url)

    if response:
        tasks = []
        soup = BeautifulSoup(response.text, "lxml")
        tags = soup.find_all("td", {"class": "topicview"})
        tag_answer = soup.find_all("td", {"class": "answer"})
        for tag_td, answer in zip(tags, tag_answer):
            answer = answer.find("script").text.strip()
            answer = re.findall(r"""\(([^\[\]]+)\)""", answer.replace("(", "", 1).strip()[:-2])[0][1:-1]
            script_lines = tag_td.find("script").text.strip().split("\n")
            task_id = int(re.search(r"\d+", script_lines[0]).group(0))
            content = re.findall(r"""\(([^\[\]]+)\)""", script_lines[1].replace("(", "", 1).strip()[:-2])[0][1:-1]
            if '<img' in content:
                start = content.index('src="') + 5
                end = content.index('">') if '">' in content else content.index('"/>')
                img = 'https://kpolyakov.spb.ru/cms/images/' + content[start:end]
                content = content[:start - 5] + f'src="data:image/png;base64, {b64encode(requests.get(img).content).decode("utf-8")}' + content[end:]
            if '<a' in content:
                pass
                # start = content.index('href="') + 5
                # end = content.index('">') if '">' in content else content.index('"/>')
                # img = 'https://kpolyakov.spb.ru/cms/images/' + content[start:end]
                # content = content[:start - 5] + f'src="data:image/png;base64, {b64encode(requests.get(img).content).decode("utf-8")}' + content[end:]
            tasks.append(content)

        return {"html": tasks}

    raise Exception("Невозможно обратиться к сайту Полякова")


def random_task(task) -> dict:
    """
    Парсит задание по ссылке типа
    https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select={task}&answers=on&varId=
    Возвращает словарь
    {"html": html_content, "id": task_id, "answer": task_answer}
    :param task: Номер задания в КИМ от 1 до 27
    :return: dict
    """
    select_id = hex(int(task, 2))[2:]
    url = f"https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select={select_id}&answers=on&varId="
    response = requests.get(url)

    if response:
        tasks = []
        soup = BeautifulSoup(response.text, "lxml")
        tags = soup.find_all("td", {"class": "topicview"})
        for tag_td in tags:
            script_lines = tag_td.find("script").text.strip().split("\n")
            task_id = re.search(r"\d+", script_lines[0]).group(0)
            html_content = re.findall(r"""\(([^\[\]]+)\)""", script_lines[1].replace("(", "", 1).strip()[:-2])
            tasks.append(html_content)

        tag_table = soup.find("table", {"class": "varanswer"})
        answer_table = {}
        for i, row in enumerate(tag_table.findAll("tr")):
            if i == 0:
                continue
            for egeno, answer in zip(row.find_all("td", {"class": "egeno"}), row.find_all("td", {"class": "answer"})):
                if answer.text:
                    answer_table[egeno.text[:-1]] = answer.text
        return {"html": tasks, 'answer': answer_table}

    raise Exception("Невозможно обратиться к сайту Полякова")


if __name__ == "__main__":
    # пример
    # a = random_task('10101')
    # print(a)
    links = ['https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=2&cat8=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=3&cat169=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=4&cat21=on&cat22=on&cat23=on&cat25=on&cat166=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=5&cat27=on&cat28=on&cat144=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=6&cat37=on&cat91=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=7&cat38=on&cat39=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=8&cat42=on&cat43=on&cat145=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=9&cat146=on&cat147=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=10&cat148=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=11&cat52=on&cat53=on&cat54=on&cat149=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=12&cat55=on&cat56=on&cat57=on&cat58=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=13&cat59=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=14&cat60=on&cat61=on&cat62=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=14&cat60=on&cat61=on&cat62=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=15&cat67=on&cat68=on&cat69=on&cat70=on&cat123=on&cat167=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=16&cat44=on&cat45=on&cat46=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=17&cat168=on&cat170=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=18&cat152=on&cat153=on&cat165=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=19&cat154=on&cat163=on&cat171=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=22&cat73=on&cat74=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=23&cat78=on&cat79=on&cat80=on&cat162=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=24&cat155=on&cat156=on&cat164=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=25&cat157=on&cat158=on&cat159=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=26&cat160=on',
             'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=27&cat161=on']
    # for link in links:
    print(collect_task(links[2])['html'])