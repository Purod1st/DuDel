from os import environ
import hashlib 
from pathlib import Path


def wsl_detect():
    if 'WSL_VERSION' in environ or 'WSL2_GUI_APPS_ENABLED' in environ or 'WSL_DISTRO_NAME' in environ:
        return True
    else:
        return False
    
def wsl_normalize(dir_path) -> str:
    prefix = '/mnt/'
    print(f'НАМ ПРИШЛО: {dir_path}')
    new_dir_path = str(dir_path).lower()
    new_dir_path = new_dir_path.replace(':\\', '/').replace('\\', '/')
    print(f'СТРОЧНОЕ НАПИСАНИЕ ДИРЕКТОРИИ {new_dir_path}')
    if new_dir_path.startswith('/mnt'):
        return
    outer_dir_path = prefix + new_dir_path
    print(f'НОВАЯ ДИРЕКТОИИЯ{outer_dir_path}')
    return outer_dir_path

def get_path():
    """
    Запрашиваем директорию для работы или устанавыливаем дефолтную
    """
    _dir_path = str(input('Введите директорию '))
    if wsl_detect():
        print('ОБНАРУЖЕН WSL, ОТПРАВЛЕНО НА ПРЕОБРАЗОВАНИЕ')
        dir_path = wsl_normalize(_dir_path)
    else:
        print('WSL НЕ ОБНАРУЖЕН')
    dir_path = Path(dir_path).resolve()
    print(f'НАРЕЗОЛВИЛИ: {dir_path}')
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