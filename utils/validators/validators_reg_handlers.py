import re


def validate_fio(fio: str) -> bool:
    if fio is None:
        return False
    else:
        if re.fullmatch("[А-ЯЁ]{1}[а-яё]+\s[А-ЯЁ]{1}[а-яё]+\s[А-ЯЁ]{1}[а-яё]+", fio):
            return True
        else:
            return False


def validate_phone(number: str) -> bool:
    if number is None:
        return False
    else:
        if re.fullmatch(r'^\+?[78]{1}\s?[(]?\d{3}[)]?\s*\d{3}\s?-?\d{2}\s?-?\d{2}$', number):
            return True
        else:
            return False
