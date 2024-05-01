'''
Напишите код, который запускается из командной строки и получает на вход
путь до директории на ПК.
Соберите информацию о содержимом в виде объектов namedtuple.
Каждый объект хранит:
○ имя файла без расширения или название каталога,
○ расширение, если это файл,
○ флаг каталога,
○ название родительского каталога.
В процессе сбора сохраните данные в текстовый файл используя
логирование.
'''
import os
from collections import namedtuple
import logging
import argparse

file_object = namedtuple("file_object", ["name", "ext", "isdir", "parent_dir"])
log = logging.getLogger(__name__)

directory = ""


def traverse_directory(directory):
    filelist: list = []
    for root, dirs, files in os.walk(os.path.normpath(directory)):
        dobj = file_object(
            os.path.basename(root),
            "",
            True,
            os.path.basename(os.path.dirname(root)),
        )
        filelist.append(dobj)
        log.info(f"Finded directory: {dobj.name} in {dobj.parent_dir}")

        for file in files:
            fobj = file_object(
                *os.path.splitext(file),
                False,
                root.split("/")[-1],
            )
            filelist.append(fobj)
            log.info(f"Finded file: {fobj.name}{fobj.ext} in {fobj.parent_dir}")
    return filelist


def init():
    parser = argparse.ArgumentParser(description="View dir")
    parser.add_argument(
        "directory", metavar="directory", type=str, nargs="?", default=""
    )
    parser.add_argument("-l", metavar="logfile", type=str, default="register.log")
    arg = parser.parse_args()

    logging.basicConfig(filename=arg.l, filemode="w", level=logging.INFO)

    return arg.directory


def print_list(lst):
    for i in lst:
        print(
            f"{'DIR' if i.isdir else 'FILE':<4} "
            f"[{i.name:^{max(map(len, [i.name for i in lst]))}}] "
            f"- ext: {i.ext[1:]:<5} "
            f"- parent_dir: {i.parent_dir}"
        )


def __main():
    direc = init()
    lst = traverse_directory(os.path.abspath(direc))
    print_list(lst)


if __name__ == "__main__":
    __main()