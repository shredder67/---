import json

def print_table(table):
    pass

def get_Pareto_set(table):
    pass

#чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]

    # 1 - вывести таблицу на экран
    # 2 - сформировать множество оптимальных решений по Парето
    # 3 - вывести отсортированную таблицу на экран + множество решений

    print(markers)
    print(table)