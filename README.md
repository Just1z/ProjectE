# Тренажёр для ЕГЭ по информатике

## Как запустить сайт:

- Получите секретный ключ сайта, запустив из консоли файл functions.py
- Создайте файл settings.ini, запишите в него следующую информацию:
```
[settings]
secret_key = <secret_key>
```
- На место <secret_key> вставьте ключ, полученный в первом пункте
- Загрузите все библиотеки из файла requirements.txt (pip install -r requirements.txt)
- Запустите файл main.py

## Как обновить базу данных задач:
- Запустите файл polyakov_parsing.py
- Подождите, пока в консоль не будет выведено "Done!"

### Ufa, 2022