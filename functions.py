""" В этом файле находятся функции, используемые в main.py"""
import os
from random import choice

from werkzeug.datastructures import FileStorage

ALL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MNEMONIC_TABLE = {
    '&forall;': '∀', '&part;': '∂', '&exist;': '∃', '&empty;': '∅',
    '&nabla;': '∇', '&amp;in;': '∈', '&notin;': '∉',
    '&ni;': '∋', '&prod;': '∏', '&sum;': '∑', '&minus;': '−',
    '&lowast;': '*', '&radic;': '√', '&prop;': '∝',
    '&infin;': '∞', '&ang;': '∠', '&and;': '∧', '&or;': '∨',
    '&cap;': '∩', '&cup;': '∪', '&int;': '∫',
    '&there4;': '∴', '&sim;': '∼', '&cong;': '≅', '&asymp;': '≈',
    '&ne;': '≠', '&equiv;': '≡', '&le;': '≤',
    '&ge;': '≥', '&sub;': '⊂', '&sup;': '⊃', '&nsub;': '⊄',
    '&sube;': '⊆', '&supe;': '⊇', '&oplus;': '⊕',
    '&otimes;': '⊗', '&perp;': '⊥'}


def generate_code(code_len=25):
    """ Возвращает случайную строку из 25 символов"""
    return "".join([choice(ALL_CHARS) for i in range(code_len)])


def normalize_html(html_text):
    """Приводит HTML в порядок для нормального отображения на сайте"""
    for key, value in MNEMONIC_TABLE.items():
        html_text = html_text.replace(key, value)
    return html_text


def does_fit(file: FileStorage, limit: int | float = float("inf")):
    """Проверяет, вместится ли файл в указанный размер в килобайтах"""
    file.seek(0, os.SEEK_END)
    size = file.tell() / 1024  # кбайт
    file.seek(0)
    print(size, limit)
    return size <= limit


if __name__ == "__main__":
    print(generate_code(40))
