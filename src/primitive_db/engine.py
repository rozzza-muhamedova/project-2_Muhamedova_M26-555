import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, delete, drop_table, insert, select, update
from primitive_db.parser import is_column_in_table, parse_set, parse_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

META_FILE = "db_meta.json" 
def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "
          "- создать запись")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> "
          "- прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where "
          "<столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - "
          "удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """Главная функция. Содержит основной цикл программы."""

    metadata = load_metadata(META_FILE)

    print_help()
    while True:
        input_command = prompt.string(">>>Введите команду: ")
        args = shlex.split(input_command)
        if len(args) == 0:
            continue
        command = args[0]
        if command == 'help':
            print_help()
        elif command == 'list_tables':
            if len(metadata) == 0:
                print("Пока нет ни одной таблицы.")
            else:
                for table in metadata:
                    print(f'- {table}')
        elif command == 'create_table':
            if len(args) < 3:
                print(f'Некорректное значение: {input_command}. '
                      f'Попробуйте снова.')
            else:
                table_name = args[1]
                colomns = args[2:]
                metadata = create_table(metadata, table_name, colomns)
                save_metadata(META_FILE, metadata)
        elif command == 'drop_table':
            if len(args) != 2:
                print(f'Некорректное значение: {input_command}. '
                      f'Попробуйте снова.')
            else:
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(META_FILE, metadata)
                
        elif command == 'select':

            if len(args) < 3 or (len(args) > 3 and args[3] != 'where'):
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue
            
            table_name = args[2]

            if args[1] != 'from':
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue

            elif table_name not in metadata:
                print(f'Ошибка: Таблицы {args[2]} не существует. Попробуйте снова.')
                continue

            where_clause = None

            if 'where' in args:
                where_str = input_command.split("where", 1)[1].strip()
                where_clause = parse_where(where_str, command)

                if where_clause is None:
                    continue
            
                valid_columns = [col["name"] for col in metadata[table_name]]
                
                if not is_column_in_table(where_clause, valid_columns, table_name):
                    continue

            table_data = load_table_data(table_name)
            result = select(table_data, where_clause)

            if result == []:
                print("Записей не найдено.")
            else:
                table = PrettyTable()
                colomns = [col["name"] for col in metadata[table_name]]
                table.field_names = colomns
                for row in result:
                    row_values = [row.get(col) for col in colomns]
                    table.add_row(row_values)
                print(table)

        elif command == 'insert':
            if len(args) < 4 or args[1] != 'into' or 'values' not in args:
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблицы {args[2]} не существует. Попробуйте снова.')
                continue
  
            start_index_values = input_command.find('(')
            end_index_values = input_command.find(')')
            values_index =input_command[start_index_values + 1:end_index_values]
            values_split = values_index.split(',')
            values = [v.strip() for v in values_split]
            table_data = load_table_data(table_name)
            result = insert(metadata, table_data, table_name, values)

            save_table_data(table_name, result)
        
        elif command == 'delete':
            if len(args) < 3:
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue

            table_name = args[2]

            if args[1] != 'from':
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue

            elif table_name not in metadata:
                print(f'Ошибка: Таблицы {args[2]} не существует.')
                continue

            if 'where' not in args:
                print(f'Ошибка: Неверный синтаксис функции {command}. '
                      f'Попробуйте снова.')
                continue
            
            where_str = input_command.split("where", 1)[1].strip()
            where_clause = parse_where(where_str, command)

            if where_clause is None:
                continue

            valid_columns = [col["name"] for col in metadata[table_name]]

            if not is_column_in_table(where_clause, valid_columns, table_name):
                continue

            table_data = load_table_data(table_name)
            result = delete(table_name, table_data, where_clause)

            save_table_data(table_name, result)

        elif command == 'update':
            if len(args) < 6 or 'set' not in args or 'where' not in args:
                print(f'Некорректное значение: {command}. Попробуйте снова.')
                continue
        
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблицы {args[1]} не существует.')
                continue

            
            set_str = input_command.split("set", 1)[1].split("where", 1)[0].strip()
            set_clause = parse_set(set_str, command)

            if set_clause is None:
                continue
            
            valid_columns = [col["name"] for col in metadata[table_name]]
                
            if not is_column_in_table(set_clause, valid_columns, table_name):
                continue

            
            where_str = input_command.split("where", 1)[1].strip()
            where_clause = parse_where(where_str, command)

            if where_clause is None:
                continue
            
            valid_columns = [col["name"] for col in metadata[table_name]]
                
            if not is_column_in_table(where_clause, valid_columns, table_name):
                continue
            
            table_data = load_table_data(table_name)
            result = update(table_name, table_data, set_clause, where_clause)

            save_table_data(table_name, result)
        
        elif command == 'info':

            if len(args) != 2:
                print(f'Некорректное значение: {command}. Попробуйте снова.')
                continue

            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблицы {args[1]} не существует.')
                continue
           
            print(f'Таблица: {table_name}')
            
            colomns = []
            for colomn in metadata[table_name]:
                colomns.append(f"{colomn['name']}:{colomn['type']}")
            print(f'Столбцы: {", ".join(colomns)}')

            table_data = load_table_data(table_name)
            print(f'Количество записей: {len(table_data)}')

        elif command == "exit":
            break
        else:
            print(f'Функции {command} нет. Попробуйте снова.')
