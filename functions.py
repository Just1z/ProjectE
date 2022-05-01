""" В этом файле находятся функции, используемые в main.py"""
from random import choice

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


def generate_code():
    """ Возвращает случайную строку из 25 символов"""
    return "".join([choice(ALL_CHARS) for i in range(25)])


def to_100(primary_points: int) -> int:
    """Перевод первичных баллов егэ во вторичные"""
    if primary_points > 29 or primary_points < 0:
        raise Exception("Некорректное количество баллов")
    table = {1: 7, 2: 14, 3: 20, 4: 27, 5: 34, 6: 40, 7: 43, 8: 46, 9: 48, 10: 51,
             11: 54, 12: 56, 13: 59, 14: 62, 15: 64, 16: 67, 17: 70, 18: 72, 19: 75, 20: 78,
             21: 80, 22: 83, 23: 85, 24: 88, 25: 90, 26: 93, 27: 95, 28: 98, 29: 100}
    return table[primary_points]


def normalize_html(html_text):
    """Приводит HTML в порядок для нормального отображения на сайте"""
    for key, value in MNEMONIC_TABLE.items():
        html_text = html_text.replace(key, value)
    return html_text
