import re
from bs4 import BeautifulSoup
from base64 import b64encode
from data import db_session
from data.tasks import Task
from colorama import init, Fore

init()
flag = False
try:
    import grequests
    flag = True
except ImportError:
    print(f"{Fore.YELLOW}Проекту не удается получить доступ к библиотеке grequests. Вероятно, она отсутствует.")
    print(f"{Fore.YELLOW}Обновление базы займёт большее время.")
    print(f"{Fore.RESET}")
import requests


def collect_task(response, number):
    """Собирает в базу данных все задания под номером number"""
    session = db_session.create_session()
    if response:
        soup = BeautifulSoup(response.text, "lxml")
        tags = soup.find_all("td", {"class": "topicview"})
        tag_answer = soup.find_all("td", {"class": "answer"})
        for tag_td, answer in zip(tags, tag_answer):
            answer = answer.find("script").text.strip()
            answer = re.findall(
                r"""\(([^\[\]]+)\)""", answer.replace("(", "", 1).strip()[:-2])[0][1:-1]
            files = []
            script_lines = tag_td.find("script").text.strip().split("\n")
            task_id = int(re.search(r"\d+", script_lines[0]).group(0))
            id = session.query(Task).filter(Task.id == task_id).first()
            content = script_lines[1].replace('document.write( changeImageFilePath(', '').replace('\'', '').strip()[
                      :-4]
            soup = BeautifulSoup(content, 'lxml')
            if soup.find('img'):
                link = 'https://kpolyakov.spb.ru/cms/images/' + soup.find('img')['src']
                soup.find('img')['src'] = 'data:image/png;base64,' + b64encode(
                    requests.get(link).content).decode("utf-8")
            if soup.find('a'):
                for a in soup.find_all('a'):
                    if not a['href'].startswith('htt'):
                        a['href'] = 'https://kpolyakov.spb.ru/cms/files/' + a['href']
                        files.append(a)
            if not id:
                task = Task(
                    id=task_id, html=str(soup.find('body')).replace('<body>', '').replace('</body>', ''),
                    answer=answer, files=' '.join(map(str, files)),
                    number=number, author_id=0)
                session.add(task)
            else:
                task = session.query(Task).filter(Task.id == task_id).first()
                task.html = str(soup.find('body')).replace('<body>', '').replace('</body>', '')
                task.answer = answer
                task.files = ' '.join(map(str, files))
                task.number = number
                task.author_id = 0
            session.commit()


if __name__ == "__main__":
    db_session.global_init("db/kege.db")
    urls = ['https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on',
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
    if flag:
        _requests = (grequests.get(url) for url in urls)
        responses = grequests.map(_requests)
        for number, response in enumerate(responses, 1):
            if number >= 18:
                number += 2
            print(f"Собираю задачи под номером {number}...")
            try:
                collect_task(response, number)
            except Exception as error:
                print(f"Ошибка: {error}")
                continue
            print(f"Задачи под номером {number} успешно собраны.")
    else:
        for number, url in enumerate(urls, 1):
            response = requests.get(url)
            if number >= 18:
                number += 2
            print(f"Собираю задачи под номером {number}...")
            try:
                collect_task(response, number)
            except Exception as error:
                print(f"Ошибка: {error}")
                continue
            print(f"Задачи под номером {number} успешно собраны.")
    print("База данных обновлена.")
