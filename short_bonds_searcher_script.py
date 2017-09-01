"""
Данный скрипт выполняет поиск облигаций, которые будут погашены в течение ближайших 50-ти дней
и выполняет расчёт доходности данных облигаций на дату погашения
"""

import requests
import datetime


def get_bonds():
    """
    Поиск облигаций
    :return: JSON c облигациями, которые будут погашены в срок до 50 дней
    """
    bond_json = requests.get("http://moex.com/iss/engines/stock/markets/bonds/securities.json").json()
    bond_list = bond_json["securities"]["data"]
    result_bond_list = []
    for bond in bond_list:
        if "0000-00-00" == bond[13]:
            continue
        mat_date = datetime.datetime.strptime(bond[13], "%Y-%m-%d")
        if mat_date.date() <= datetime.datetime.now().date() + datetime.timedelta(days=50) \
                and mat_date.date() != datetime.datetime.now().date():
            result_bond_list.append(bond)
    return result_bond_list


def calc_yield(bond_list):
    """
    Расчёт доходности облигаций
    """
    tax = 0.13  # Налог
    for bond in bond_list:
        h = float(bond[10])  # Цена погашения
        c = float(bond[5])  # Сумма купонных выплат. Так как облигация покупается за несколько дней до погашения, то сумма равна величине купона
        p = float((bond[10]/100)*bond[17] if bond[17] else bond[10]) + float(bond[7])  # Цена покупки + НКД
        mat_date = datetime.datetime.strptime(bond[13], "%Y-%m-%d")  # Дата погашения
        t = (mat_date.date() - datetime.datetime.now().date()).days  # Количество дней владения облигацией
        bond_yield = (h + c - p) - c * tax  # Доход
        r = (bond_yield/p)*(365/t)*100  # Годовая доходность
        bond.append(round(bond_yield, 2))
        bond.append(round(r, 2))
        bond.append(t)


def print_bond_list(bond_list):
    """
    Печать списка облигаций
    :param bond_list: список облигаций
    """
    print("=" * 186)
    print("|%15s|%35s|%15s|%15s|%15s|%15s|%20s|%15s|%15s|%15s|" % ("ISIN", "Наименование", "Номинал", "Величина купона", "НКД", "Дата погашения", "Дней до погашения", "Цена закрытия", "Доход", "Доход в %"))
    print("=" * 186)
    for bond in bond_list:
        print("|%15s|%35s|%15s|%15s|%15s|%15s|%20s|%15s|%15s|%15s|" % (bond[0], bond[20], bond[10], bond[5], bond[7], bond[13], bond[39], bond[17], bond[37], bond[38]))
    print("=" * 186)


def main():
    """
    Главная функция
    """
    bond_list = get_bonds()
    calc_yield(bond_list)
    print_bond_list(bond_list)


if __name__ == "__main__":
    main()
