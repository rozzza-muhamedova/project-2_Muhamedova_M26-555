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

def drop_table(metadata, table_name):
    """Удаляет таблицу."""
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена.')
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    return metadata
