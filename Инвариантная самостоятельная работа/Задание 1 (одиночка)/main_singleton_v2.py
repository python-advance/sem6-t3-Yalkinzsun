from urllib.request import urlopen
from xml.etree import ElementTree as ET
import time


def get_currencies(currencies_ids_lst=['R01239', 'R01235', 'R01035']):
    cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
    result = {}
    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()
    valutes = root.findall('Valute')
    for el in valutes:
        valute_id = el.get('ID')
        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            result[valute_id] = valute_cur_val
    return result


class CurrencyBoard:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CurrencyBoard.__instance == None:
            CurrencyBoard()
        return CurrencyBoard.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.currencies = ['R01239', 'R01235', 'R01035']
        self.rates = get_currencies(self.currencies)
        self.timesaver = time.time()
        if CurrencyBoard.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CurrencyBoard.__instance = self

    def get_currency_from_cache(self, code):
        return self.rates.setdefault(code)

    def get_new_currency(self, code):
        self.currencies.append(code)
        self.rates.update(get_currencies([code]))
        return {code: self.rates[code]}

    def update(self):
        self.rates.clear()
        self.rates = get_currencies(self.currencies)
        return self.rates

    def check(self):
        if time.time() - self.timesaver > 300:
            return self.update()
        else:
            print('Последенее обновление было меньше 5 минут назад!')


if __name__ == "__main__":
    X = CurrencyBoard()
    print(f'Текущие курсы: {X.rates}')
    print(f'Получение валюты с ID = R01239 из кэша: {X.get_currency_from_cache("R01239")}')
    print(f'Добавление новой валюты с ID = R01375: {X.get_new_currency("R01375")}')
    print(f'Текущие курсы: {X.rates}')
    print(f'Принудительное обновление всех курсов: {X.update()}')
    print('Ждём 2 минуты...')
    time.sleep(120)
    print('Проверяем, можно ли обновить курсы:\n', X.check())
    print('Ждём ещё 3 минуты...')
    time.sleep(180)
    print('Проверяем, можно ли обновить курсы:\n', X.check())
