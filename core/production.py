import xml.etree.ElementTree as ET
from collections import OrderedDict
import json
from .class_labyak import LabYak

def production_calculation(days, xml_file, stock_file, herd_file) -> None:
    """
    The core logic of computing the stock and herd info.
    It reads the yak info from xml_file and updates the result in stock_file and herd_file.

    Args:
        days (str): the elapsed days.
        xml_file (str): the herd xml file path.
        stock_file (str): the stock json file path.
        herd_file (str): the herd json file path.
    """
    yak_names = []
    yak_ages = []
    milk_production = []
    wool_production = []
    age_lastshaving = []
    age_aftershaving = []
    herd_info = []
    product_info = OrderedDict()

    with open(xml_file, encoding='UTF-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        for child in root:
            yak_names.append(str(child.attrib["name"]))
            yak_ages.append(float(child.attrib["age"]) if '.' in child.attrib["age"] else int(child.attrib["age"]))

    # Create yak objects for all available yaks
    yak_objs = [LabYak(name, age) for name, age in zip(yak_names, yak_ages)]

    for yak_obj in yak_objs:
        milk, wool, age_last_shaved, age = yak_obj.yak_production(days)
        milk_production.append(milk)
        wool_production.append(wool)
        age_lastshaving.append(age_last_shaved)
        age_aftershaving.append(age)

    product_info["milk"] = sum(milk_production)
    product_info["skins"] = sum(wool_production)

    for idx in range(len(yak_names)):
        yak_info = OrderedDict()
        yak_info['name'] = yak_names[idx]
        yak_info['age'] = age_aftershaving[idx]
        yak_info['age-last-shaved'] = age_lastshaving[idx]
        herd_info.append(yak_info)

    with open(stock_file, 'w', encoding='UTF-8') as f:
        json.dump((product_info), f)

    with open(herd_file, 'w', encoding='UTF-8') as f:
        json.dump(({'herd': herd_info}), f)