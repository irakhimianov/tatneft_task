from typing import Optional


def is_prime(num: int) -> bool:
    """
    Проверка числа на то, является ли оно простым
    :param num: Число для проверки
    :type num: int
    :return: Истина/ложь
    :rtype: bool
    """
    if num <= 1:
        return False

    for i in range(2, int(num ** 0.5 + 1)):
        if num % i == 0:
            return False
    return True


def get_prime_numbers(num: int) -> list[Optional[int]]:
    """
    Получение списка простых чисел по переданное число, НЕ включительно
    :param num: Правая граница списка простых чисел
    :return: Список простых чисел
    :rtype: list[int], optional
    """
    return [n for n in range(num) if is_prime(n)]
