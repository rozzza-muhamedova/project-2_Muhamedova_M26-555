import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata

META_FILE = "db_meta.json" 
def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
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
                print(f'Некорректное значение: {input_command}. Попробуйте снова.')
            else:
                table_name = args[1]
                colomns = args[2:]
                metadata = create_table(metadata, table_name, colomns)
                save_metadata(META_FILE, metadata)
        elif command == 'drop_table':
            if len(args) != 2:
                print(f'Некорректное значение: {input_command}. Попробуйте снова.')
            else:
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(META_FILE, metadata)
        elif command == "exit":
            break
        else:
            print(f'Функции {command} нет. Попробуйте снова.')
