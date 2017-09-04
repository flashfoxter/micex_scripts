"""
Данный скрипт выполняет поиск облигаций 1-го эшелона и сортирует по доходности
"""

import requests
from operator import itemgetter


def get_1st_level_bonds():
    """
    Поиск облигаций
    :return: JSON c облигациями 1-го эшелона
    """
    bond_json = requests.get("http://moex.com/iss/engines/stock/markets/bonds/securities.json").json()
    bond_list = bond_json["securities"]["data"]
    result_bond_list = []
    for bond in bond_list:
        if 1 != bond[34]:
            continue
        result_bond_list.append(bond)
    return result_bond_list


def print_bond_list(bond_list):
    """
    Печать списка облигаций
    :param bond_list: список облигаций
    """
    print("=" * 169)
    print("|%15s|%35s|%15s|%15s|%15s|%15s|%20s|%30s|" % ("ISIN", "Наименование", "Номинал", "Величина купона", "НКД", "Дата погашения", "Цена закрытия", "Доходность по оценке пред. дня"))
    print("=" * 169)
    for bond in bond_list:
        print("|%15s|%35s|%15s|%15s|%15s|%15s|%20s|%30s|" % (bond[0], bond[20], bond[10], bond[5], bond[7], bond[13], bond[17], bond[4]))
    print("=" * 169)


def main():
    """
    Главная функция
    """
    bond_list = get_1st_level_bonds()
    print_bond_list(sorted(bond_list, key=itemgetter(4), reverse=True))


if __name__ == "__main__":
    main()