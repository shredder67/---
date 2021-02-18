import json

SHIFT = ('-----------------------------------------------'
'----------------------------')

# выводит таблицу
def print_table(table):
    i = 1
    print(SHIFT)
    print('  1',end='\t')
    for j in range(2, len(table) + 1):
        print(j,end='\t')
    print()
    
    for row in table:
        print(i, end=' ')
        for v in row:
            print(v, end='\t')
        print()
        i += 1
    print(SHIFT, end='\n\n')

# сравнивает две альтернативы
def compare(alt1, alt2):
    flag = False
    for i in range(len(alt1)):
        if alt1[i] > alt2[i]: 
            flag = True
        elif alt1[i] < alt2[i]: 
            return False # неопределенность
    return flag 

def get_Pareto_table(markers, table):

    table_copy = [table[i].copy() for i in range(len(table))]
    
    # корректировка данных для удобства сравнения
    for i in range(len(table_copy)):
        for j in range(len(table_copy[i])):
            if(not markers[j]):
                table_copy[i][j] = - table_copy[i][j]

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

# чтение файла с данными
with open('pr1_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    markers = content["comp_markers"]
    table = content["data"]
    #таблица, храняшая все критерии по индексам
    t_table = [list(table[i].values())[1:] for i in range(len(table))]
    print_table(t_table)

    res_table = get_Pareto_table(markers, t_table)
    print_table(res_table)
    
