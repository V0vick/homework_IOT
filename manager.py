import os                                   #перевірка існування файлу ос.паз.екзіст
import logging                              #виведення помилок в файл\консоль
from functools import wraps                 #зберігає ім'я і документацію функції при використанні декоратора

#винятки#

class FileCorrupted(Exception):
    "Файл пошкоджений"                      # створення власних винятків
    pass                                    # тип помилки (не ситається або пошкоджений)

class FileNotFound(Exception):
    "Файл не знайдено"                      # помилка якщо файлу немає
    pass

def logged(exception_type, mode="file"):    #приймає тип помилки і режим логування
    def decorator(func):                    #перехоплює виклик функцї
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:                            
                return func(*args, **kwargs)    # спроба виконання функції. все гуд - повернення результату   
            except exception_type as e:     # якщо є помилка - ловимр її щоб не зламалась програма, для пов. користувача,  запису помилки в лог
                logger = logging.getLogger(func.__name__)
                logger.setLevel(logging.ERROR)  # створємо логер, ерор

                if mode == "console":
                    handler = logging.StreamHandler()
                elif mode == "File":
                    handler = logging.FileHandler("file_operation.log")
                else: 
                    raise ValueError("Невідомий режим лоогування")  #логування в консоль або в файл
                
                formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formater)
                logger.addHandler(handler)          #форматуємо лог, ддодаємо обробник

                logger.error(f"Помилка: {str(e)}")
                raise                       #запис помилки в лог
        return wrapper
    return decorator

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                pass                       #зберігає шлях до файлу, показує помилку якщо файлу нема
    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise FileCorrupted(f"Не вдалося прочитати файл: {e}")  #читання вмісту файлу, при наявності виводить пошкодження
        
    @logged(FileCorrupted, mode="console")
    def write(self, content):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise FileCorrupted(f"Не вдалося записати у фал: {e}")  #перезаписує файл новим вмістом
        
    @logged(FileCorrupted, mode="console")
    def append(self, content):
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
                raise FileCorrupted(f"Не вдалося дописати у файл: {e}") #додає текст у кінець файлу
        
if __name__ == "__main__":

    try:
        open ("test.txt", "a").close()
        fm = FileManager("test.txt")
        fm.write("Добрий день!")
        fm.append("Ми з команди 'RedBULL' ")
        print(fm.read())
    except FileNotFound as e:
        print(f"X {e}")
    except FileCorrupted as e:
        print(f"Файл пошкоджено {e}")