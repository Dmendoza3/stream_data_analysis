import os
import sys

#files = os.listdir(main_dir)

filtered_extensions = ("txt")

def folder_iterator(main_dir="./", filter=""):
    files = os.scandir(main_dir)
    for file in files:
        filename = file.name
        is_directory = file.is_dir()
        full_path = file.path

        split_filename = filename.split(".")
        extension = split_filename[-1]
        if filter:
            if extension not in filter:
                continue

        yield (filename, is_directory, full_path)


if __name__ == "__main__":
    for file in folder_iterator("./", "txt"):
        print(file)