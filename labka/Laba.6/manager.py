import os                                   
import logging                              
from functools import wraps                 

#винятки#

class FileCorrupted(Exception):
    "Файл пошкоджений"                      
    pass                                    

class FileNotFound(Exception):
    "Файл не знайдено"                      
    pass

def logged(exception_type, mode="file"):    
    def decorator(func):                    
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:                            
                return func(*args, **kwargs)       
            except exception_type as e:     
                logger = logging.getLogger(func.__name__)
                logger.setLevel(logging.ERROR)  

                if mode == "console":
                    handler = logging.StreamHandler()
                elif mode == "File":
                    handler = logging.FileHandler("file_operation.log")
                else: 
                    raise ValueError("Невідомий режим лоогування")  
                
                formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formater)
                logger.addHandler(handler)          

                logger.error(f"Помилка: {str(e)}")
                raise                       
        return wrapper
    return decorator

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                pass                       
    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise FileCorrupted(f"Не вдалося прочитати файл: {e}")  
        
    @logged(FileCorrupted, mode="console")
    def write(self, content):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise FileCorrupted(f"Не вдалося записати у фал: {e}")  
        
    @logged(FileCorrupted, mode="console")
    def append(self, content):
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
                raise FileCorrupted(f"Не вдалося дописати у файл: {e}") 
        
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