from primitive_db.decorators import (
    confirm_action,
    handle_db_errors,
    log_time,
)


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу с колонками."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    else:
        clmns_tbl = []
        count = 0
        for clmn in columns:
            clmn_parts = clmn.split(":")
            if len(clmn_parts) != 2:
                print(f'Некорректное значение: {clmn}. Попробуйте снова.')
                return metadata
            else:
                if clmn_parts[1] not in ('int', 'str', 'bool'):
                    print(f'Некорректное значение: {clmn_parts[1]}. Попробуйте снова.')
                    return metadata
                else:
                    clmns_tbl.append({"name": clmn_parts[0], "type": clmn_parts[1]})
                    if clmn_parts[0].lower() == 'id':
                        count += 1
        if count ==  0:
            clmns_tbl = [{"name": "ID", "type": "int"}] + clmns_tbl
        else:
            clmns_tbl = sorted(clmns_tbl, key=lambda x: x.get("name").lower() != 'id')
        metadata[table_name] = clmns_tbl
        clmns_print = ", ".join([f"{c['name']}:{c['type']}" for c in clmns_tbl])
        print(f'Таблица "{table_name}" успешно создана со столбцами: {clmns_print}.')
        return metadata

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу."""
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена.')
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    return metadata

@handle_db_errors
@log_time
def insert(metadata, table_data, table_name, values):
    """Cоздает запись в таблице."""
    if table_data is None:
        table_data = []

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data
    
    if len(values) != len(metadata[table_name]) - 1:
        print(f'Ошибка: Количество переданных значений не соответствует '
              f'количеству столбцов в таблице {table_name}.')
        return table_data
    
    if len(table_data) == 0:
        new_id = 1
    else:
        new_id = max(row["ID"] for row in table_data) + 1
    new_row = {"ID":new_id}
    for i in range(1, len(metadata[table_name])):
        exp_type = metadata[table_name][i]["type"]
        value = values[i - 1]
        if exp_type == 'int':
            conv_value = int(value)
        elif exp_type == 'bool':
            if value.lower() == 'true':
                conv_value = True
            elif value.lower() == 'false':
                conv_value = False
            else:
                print(f'Ошибка: Неверный тип данных для {value}')
                return table_data
        elif exp_type == 'str':
            conv_value = value.strip('"')
        new_row[metadata[table_name][i]["name"]] = conv_value
    table_data.append(new_row)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу {table_name}.')
    return table_data

@handle_db_errors
@log_time
def select(table_data, where_clause=None, cache_func=None):
    """Читает записи из таблицы по условию."""
    
    if table_data is None:
        return []

    cache_key = str(where_clause)

    def get_filtered_data():
        if where_clause is None:
            return table_data
        else:
            for key, value in where_clause.items():
                key_val = key
                value_val = value
            filtered_table_data = []
            for dic in table_data:
                if dic.get(key_val) == value_val:
                    filtered_table_data.append(dic)
        return filtered_table_data
    
    if cache_func is not None:
        return cache_func(cache_key, get_filtered_data)
    else:
        return get_filtered_data()

@handle_db_errors
def update(table_name, table_data, set_clause, where_clause):
    """Обновляет записи по условию."""
    if table_data is None: 
        table_data = [] 

    for key, value in where_clause.items():
            where_key_val = key
            where_value_val = value
    for key, value in set_clause.items():
            set_key_val = key
            set_value_val = value

    updated_count = 0

    for dic in table_data:
        if dic.get(where_key_val) == where_value_val:
            dic[set_key_val]= set_value_val
            print(f'Запись с ID={dic["ID"]} в таблице {table_name} успешно обновлена.')
            updated_count += 1
    if updated_count == 0:  # <--- ПРОВЕРКА
        print(f'Ошибка: Записей с {where_key_val} = {where_value_val} не найдено.')
        
    return table_data

@confirm_action("удаление записи")
@handle_db_errors
def delete(table_name, table_data, where_clause):
    """Удаляет записи по условию."""
    if table_data is None: 
        table_data = [] 
    new_table_data = []
    deleted_count = 0
    for key, value in where_clause.items():
            where_key_val = key
            where_value_val = value
    for dic in table_data:
        if dic.get(where_key_val) != where_value_val:
            new_table_data.append(dic)
        else:
            print(f'Запись с ID={dic["ID"]} успешно удалена из таблицы "{table_name}".')
            deleted_count += 1
    if deleted_count == 0:
        print(f'Ошибка: Записей с {where_key_val} = {where_value_val} не найдено.')
    return new_table_data