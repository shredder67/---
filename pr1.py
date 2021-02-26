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

def copy_table(table):
    return [table[i].copy() for i in range(len(table))]

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

    table_copy = copy_table(table)
    
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
            if borders[i][0] > data[el - 1][i] or borders[i][1] < data[el - 1][i]:
                break
        else:
            opt_set.add(el)
    return opt_set

# субоптимизация
def optimize_pareto_set_2(unopt_set, data, main_cr, borders):
    # модифицируем таблицу информации о номере альтернативы
    mod_data = copy_table(data)
    for i in range(len(data)):
        mod_data[i].insert(0, i)
    
    # удаление из таблицы лишних данных
    i = 0
    while i < len(mod_data):
        if (mod_data[i][0] + 1) not in unopt_set:
            del mod_data[i]
        else:
            i += 1
    
    # сортируем таблицу по основному критерию
    mod_data = sorted(mod_data, key = lambda row: row[main_cr], reverse = False)

    # вычленяем альтернативы с максимальным основным критерием
    res = set()
    i = 0
    while mod_data[i][main_cr] == mod_data[0][main_cr]:
        res.add(mod_data[i][0] + 1)
        i += 1

    if len(res) == 1:
        return res

    # если в множестве больше одного элемента, требуется проверить остальные на соответствие нижним границам
    # TODO: finish subopt with low/high border check depending on tendency type    

# лексикографическая оптимизация
def optimize_pareto_set_3(table):
    pass

# чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]
    borders = content["borders"]
    #таблица, храняшая все критерии по индексам
    t_table = [list(table[i].values())[1:] for i in range(len(table))]
    cr_names = list(table[0].keys())
    print_table(t_table)

    res_table = get_pareto_table(markers, t_table)
    print_table(res_table)

    raw_set = get_raw_pareto_set(res_table)
    print('Неоптимизированное множество Парето:', raw_set)

    opt_set = optimize_pareto_set_1(raw_set, t_table, borders)
    print('Множество, оптимизированное с помощью метода границ:', opt_set)

    # main_criteria = input("Введите главный критерий для субоптимизации: ")
    main_criteria = "Урон"

    opt_set = optimize_pareto_set_2(raw_set, t_table, cr_names.index(main_criteria) - 1, borders)
    print('Множество, оптимизированное с помощью метода субоптимизации:', opt_set)

