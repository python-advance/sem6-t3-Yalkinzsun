import json
from urllib.request import urlopen
from xml.etree import ElementTree as ET
import xmltodict


def CurrenciesJSONData(f):
    def wrapper(*args, **kwargs):
        return json.dumps(f(*args, **kwargs), sort_keys=True, indent=4, ensure_ascii=False)
    return wrapper


class CurrenciesXMLData():
    @CurrenciesJSONData
    def get_data(self):
        cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
        root = ET.tostring(ET.parse(cur_res_str).getroot(), encoding="unicode")
        return xmltodict.parse(root, encoding='utf-8')

    def serialize(self):
        with open('file.json', 'a', encoding='utf-8') as f:
            json.dump(json.dumps(self.get_data(), ensure_ascii=False), f)


if __name__ == "__main__":
    X = CurrenciesXMLData()
    print(X.get_data())
    X.serialize()
