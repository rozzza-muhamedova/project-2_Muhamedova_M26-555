import time


def handle_db_errors(func):
    """Обрабатывает исключения и выводит сообщения об ошибках."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, "
                  "база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Запрашивает у пользователя подтверждение для опасных операций."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer.lower() == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                return None 
        return wrapper
    return decorator

def log_time(func):
    """Замеряет время выполнения функции и выводит его в консоль."""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.3f} " 
              f"секунд.")
        return result
    return wrapper

def create_cacher():
    """Создает функцию для кэширования результатов по ключу."""
    cache = {}
    
    def cache_result(key, value_func):
        if key in cache:
            #print("Берем из кэша.")
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            return result
            
    return cache_result