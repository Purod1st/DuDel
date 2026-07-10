import hashlib 
import time
from pathlib import Path


def get_path():
    """
    Запрашиваем директорию для работы или устанавыливаем дефолтную
    """
    _dir_path = str(input('Введите директорию '))
    dir_path = Path(_dir_path).resolve()
    return dir_path

def get_dir(dir_path):
    """
    Получаем директоию, в которой будем проводить работу
    и отдаём инфу о файлах
    """
    files = []
    #dirs = []
    if Path(dir_path).is_dir(): #Это директория
        for i in Path(dir_path).iterdir():
            if Path(i).is_file():
                files.append(i)
            if not Path(i).is_file():
                continue
            # if Path(i).is_dir(): TODO Рекурсивно по директориям
            #     dirs.append(i)
        return files
    else:
        print('Это не директория')
        return


def dir_print_info(dir_path, files):
    """
    Вывод инфомрации о директории
    """
    print(f'В директории {dir_path} имеется {len(files)} файлов')
    #print('По какому принципу проводим чистку?')


def get_hash(file):
    hash = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b''):
            hash.update(chunk)
    return hash.hexdigest()

def process_files(files):
    hashes = []
    rasstrel = []
    for i in files:
        filesize = i.stat().st_size
        print(f'Обрабатываем файл: {i}\nРазмер файла: {filesize} Byte')
        filehash = get_hash(i)
        if filehash not in hashes:
            hashes.append(filehash)
        else:
            rasstrel.append(i)
        print(f'Файл {i} обработан')
    return rasstrel

def delete_files(rasstrel):
    for i in rasstrel:
        print(f'Удаляем файл {i}')
        Path(i).unlink()
    print('Удаление завершено')
    return
    

def killing_machine(rasstrel):
    print(f'Найдено {len(rasstrel)} дубликатов:')
    for i in rasstrel:
        print(i)
    print(f'\nУдалить их? (Да\Нет)')
    user_input = str(input())
    if user_input == 'Да':
        delete_files(rasstrel)
    if not user_input == 'Да':
        return
    return

def main():
    print('Работа скрипта начата')
    one = get_path()
    two = get_dir(one)
    dir_print_info(one, two)
    three = process_files(two)
    killing_machine(three)
    print('Работа скрипта окончена')

if __name__ == "__main__":
    main()

# TODO
# получаем хеши слайсами по 100
#храним в словаре хеш:путь
#получили 100 --> удалили дубли --> получили следующие 100 --> повторять пока не кончатся
