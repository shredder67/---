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

# исключает все альтернативы из таблицы, не включенные в множество
def cut_table(opt_set, table):
    i = 0
    while i < len(table):
        if (table[i][0]) not in opt_set:
            del table[i]
        else:
            i += 1

# модифицирует упорядоченную таблицу альтернатив столбцом из номеров альтернатив
def add_table_index(table):
    for i in range(len(table)):
        table[i].insert(0, i + 1)

# субоптимизация
def optimize_pareto_set_2(unopt_set, data, main_cr, markers, borders):
    # модифицируем таблицу информации о номере альтернативы
    mod_data = copy_table(data)
    add_table_index(mod_data)
    
    # удаление из таблицы лишних данных
    cut_table(unopt_set, mod_data)
    # сортируем таблицу по основному критерию
    mod_data = sorted(mod_data, key = lambda row: row[main_cr + 1]*(-markers[main_cr]))
    # вычленяем альтернативы с максимальным основным критерием
    res = set()
    i = 0
    while mod_data[i][main_cr + 1] == mod_data[0][main_cr  + 1]:
        res.add(mod_data[i][0])
        i += 1

    # требуется проверить альтернативы на соответствие нижним границам
    cut_table(res, mod_data)
    i = 0
    while i < len(mod_data):
        alt = mod_data[i]
        j = 0
        while j < len(borders):
            # проверка j-того критерия у i-той альтернативы на попадание в установленные границы
            if alt[j + 1] < borders[j][0]:
                res.discard(alt[0])
                break
            j += 1
        i += 1
    return res

# лексикографическая оптимизация
def optimize_pareto_set_3(unopt_set, data, priorities, markers):
    #удаляем лишние альтернативы
    mod_data = copy_table(data)
    add_table_index(mod_data)
    cut_table(unopt_set, mod_data)

    res = unopt_set.copy()
    i = 0
    # пока в множестве не останется один элемент или не закончатся критерии
    while len(res) > 1 or i == len(priorities):
        cr = priorities[i]
        mod_data = sorted(mod_data, key = lambda row : row[cr + 1]*(-markers[cr]))
        j = len(mod_data) - 1
        while mod_data[j][cr + 1] < mod_data[0][cr + 1]:
            res.discard(mod_data[j][0])
            j -= 1
        i += 1

    return res
            

# чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]
    borders = content["borders"]
    priorities = content["priorities"]
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

    opt_set = optimize_pareto_set_2(raw_set, t_table, cr_names.index(main_criteria) - 1, markers, borders)
    print('Множество, оптимизированное с помощью метода субоптимизации:', opt_set)

    opt_set = optimize_pareto_set_3(raw_set, t_table, priorities, markers)
    print('Множество, оптимизированное с помощью лексикографического анализа:', opt_set)

