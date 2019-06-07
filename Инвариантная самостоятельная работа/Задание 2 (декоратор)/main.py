from urllib.request import urlopen
from xml.etree import ElementTree as ET
import json


class CurrenciesXMLData:
    """Класс для получения данных о валютах с сайта Центробанка РФ"""

    def __init__(self):
        self.currencies_ids_lst = ['R01239', 'R01235', 'R01035']

    def get_currencies(self):
        cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
        result = {'Valute': []}
        cur_res_xml = ET.parse(cur_res_str)
        root = cur_res_xml.getroot()
        valuta = root.findall('Valute')
        for el in valuta:
            valuta_id = el.get('ID')
            if str(valuta_id) in self.currencies_ids_lst:
                concrete_valuta = {}
                concrete_valuta.update({'ID': valuta_id})

                valuta_cur_val = el.find('Value').text
                concrete_valuta.update({'Value': valuta_cur_val})

                valuta_cur_name = el.find('Name').text
                concrete_valuta.update({'Name': valuta_cur_name})

                valuta_cur_namcode = el.find('NumCode').text
                concrete_valuta.update({'NumCode': valuta_cur_namcode})

                valuta_cur_charcode = el.find('CharCode').text
                concrete_valuta.update({'CharCode': valuta_cur_charcode})

                result["Valute"].append(concrete_valuta)
        return result


class CurrenciesJSONData:
    """Декоратор, позволяющий преобразовывать и сохранять данные о курсах валют в формате JSON."""

    def __init__(self, obj):
        self.obj = obj

    def get_currencies(self):
        return json.dumps(self.obj.get_currencies(), sort_keys=True, indent=3, ensure_ascii=False)

    def serialize(self):
        with open('file.json', 'a', encoding='utf-8') as file:
            file.write(self.get_currencies())


if __name__ == "__main__":
    X = CurrenciesXMLData()
    X = CurrenciesJSONData(X)
    print(X.get_currencies())
    X.serialize()

