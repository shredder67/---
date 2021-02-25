import json

# выводит таблицу
def print_table(table):
    i = 1
    shift = '-'*(8*len(table[0]) + 3)
    print(shift)
    print('\t1',end='\t')
    for j in range(1, len(table[0])):
        print(j + 1,end='\t')
    print()
    print(shift)
    for row in table:
        print(i, ' |', end='\t')
        for v in row:
            print(v, end='\t')
        print()
        i += 1
    print(shift, end='\n\n')

# сравнивает две альтернативы
def compare(alt1, alt2):
    flag = False
    for i in range(len(alt1)):
        if alt1[i] > alt2[i]: 
            flag = True
        elif alt1[i] < alt2[i]: 
            return False # неопределенность
    return flag 

def get_pareto_table(markers, table):

    table_copy = [table[i].copy() for i in range(len(table))]
    
    # корректировка данных для удобства сравнения
    for i in range(len(table_copy)):
        for j in range(len(table_copy[i])):
                table_copy[i][j] *= markers[j]

    res = [['x' for _ in range(len(table_copy))] for _ in range(len(table_copy))]
    
    for i in range(len(res)):
        for j in range(i):
            c1 = compare(table_copy[i], table_copy[j])
            c2 = compare(table_copy[j], table_copy[i])
            
            if not c1 and not c2: 
                # несравниваемы по-любому
                res[i][j] = 'н'
                res[j][i] = 'н'
            elif c1:
                #al1 доминирует над alt2
                res[i][j] = i + 1
            else:
                res[j][i] = j + 1    
    return res 

def get_raw_pareto_set(table):
    res_set = set()
    for row in table:
        for el in row:
            if isinstance(el, int):
                res_set.add(el)
    return res_set

# метод верхних/нижних границ
def optimize_pareto_set_1(unopt_set, data, borders):
    opt_set = set()
    for el in unopt_set:
        for i in range(len(data[el])):
            if borders[el][0] > data[el][i] or borders[el][1] < data[el][i]:
                break
        else:
            opt_set.add(el)
    return opt_set
        

# субоптимизация
def optimize_pareto_set_2(table):
    pass

# лексикографическая оптимизация
def optimize_pareto_set_3(table):
    pass

# чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]
    #таблица, храняшая все критерии по индексам
    t_table = [list(table[i].values())[1:] for i in range(len(table))]
    print_table(t_table)

    res_table = get_pareto_table(markers, t_table)
    print_table(res_table)

    raw_set = get_raw_pareto_set(res_table)
    print('Неоптимизированное множество Парето:', raw_set)

    borders = [(300, 500), (200, 300), (3, 8), (0.2, 0.5),
                (2, 3.5), (700, 1400), (25, 50), (1100, 1750),
                (100, 250), (300, 400)]

    opt_set = optimize_pareto_set_1(raw_set, t_table, borders)
    print('Множество, оптимизированное с помощью метода границ:', opt_set)
