import os
import csv

main_dir = "./" #sys.argv[2]

files = os.listdir(main_dir)


search_text = "tskr"
out_list = open(f"list_found({search_text}).log", "w", encoding="utf-8")

for file in files:
    if len(file.split(".")) == 3:
        name, n, ext = file.split(".")
        if ext == "txt" and n == "n1":
            i_file = open(main_dir + "/" + file, "r", encoding="utf-8")

            headers = next(i_file)

            print("Reading", name, "...")
            for row in i_file:
                clean_row = row.replace("(", "").replace(")", "").replace("'","").replace("\n", "")
                word, count = clean_row.split(", ")

                if word == search_text:
                    print(file, count, sep=",", file=out_list)

