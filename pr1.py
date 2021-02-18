import json

SHIFT = ('-----------------------------------------------'
'----------------------------')

#выводит таблицу
def print_table(table):
    i = 1
    print(SHIFT)
    for row in table:
        print(i, end=' ')
        for v in row:
            print(v, end='\t')
        print()
        i += 1
    print(SHIFT, end='\n\n')

#сравнивает две альтернативы (???)
def compare(alt1, alt2):
    flag = False
    for i in range(len(alt1)):
        if alt1[i] > alt2[i]: flag = True
        elif alt1[i] < alt2[i]: return False # неопределенность
    return flag # alt1 - доминирующий, alt2 - доминируемый

def get_Pareto_set(markers, table):
    # корректировка данных для удобства сравнения
    for i in range(len(table)):
        for j in range(len(table[i])):
            if(not markers[j]):
                table[i][j] = - table[i][j]

    res = [[] for _ in range(len(table))]
    for i in range(len(table)):
        for j in range(len(table[i])):
            c = compare(table[i], table[j])
            if(c > 0):
                pass
            elif c < 0:
                pass
            else:
                pass
    return res
    

#чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]

    #таблица, храняшая все критерии по индексам
    t_table = [list(table[i].values())[1:] for i in range(len(table))]
    get_Pareto_set(markers, t_table)
    # 1 - вывести таблицу на экран
    # 2 - сформировать множество оптимальных решений по Парето
    # 3 - вывести отсортированную таблицу на экран + множество решений
