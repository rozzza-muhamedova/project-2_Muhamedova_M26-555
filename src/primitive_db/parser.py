def parse_where(where_clause_str, command):
    """Разбирает where условие."""
    where_clause_str_split = where_clause_str.split("=")
    where_clause = {}
    if len(where_clause_str_split) != 2:
        print(f'Ошибка: Неверный синтаксис функции {command}. Попробуйте снова.')
        return None
    else:
        key = where_clause_str_split[0].strip()
        val = where_clause_str_split[1].strip()
        
    if key == "" or val == "":
        print(f'Ошибка: Неверный синтаксис функции {command}. Попробуйте снова.')
        return None

    if val.startswith('"'):
        val_strip = val.strip('"')
        where_clause[key] = val_strip
    elif val.startswith("'"):
        val_strip = val.strip("'")
        where_clause[key] = val_strip
    elif val.lower() == 'true':
        where_clause[key] = True
    elif val.lower() == 'false':
        where_clause[key] =  False
    else:
        try:
            val_conv = int(val)
            where_clause[key] = val_conv
        except ValueError:
            print(f'Ошибка: Неверный синтаксис функции {command}. Попробуйте снова.')
            return None
    return where_clause


def parse_set(set_clause_str, command):
    """Разбирает set условие."""
    set_clause_str_split = set_clause_str.split("=")
    set_clause = {}
    if len(set_clause_str_split) != 2:
        print(f'Ошибка: Неверный синтаксис функции {command}. Попробуйте снова.')
        return None
    else:
        key = set_clause_str_split[0].strip()
        val = set_clause_str_split[1].strip()
        
    if key == "" or val == "":
        print(f'Ошибка: Неверный синтаксис функции {command}. Попробуйте снова.')
        return None

    if val.startswith('"'):
        val_strip = val.strip('"')
        set_clause[key] = val_strip
    elif val.startswith("'"):
        val_strip = val.strip("'")
        set_clause[key] = val_strip
    elif val.lower() == 'true':
        set_clause[key] = True
    elif val.lower() == 'false':
        set_clause[key] =  False
    else:
        try:
            val_conv = int(val)
            set_clause[key] = val_conv
        except ValueError:
            print('Ошибка: Некорректный синтаксис для "set".')
            return None
    return set_clause

def is_column_in_table(clause_colomn, valid_columns, table_name):
    """Проверяет наличие колонок в таблице."""
    if clause_colomn is None:
        return True 
        
    for key in clause_colomn.keys():
        if key not in valid_columns:
            print(f'Ошибка: Колонки "{key}" не существует в таблице "{table_name}".')
            return False
    return True