import os

list_dir = os.listdir(".")

o_file = open("transcript_join.csv", "w", encoding="utf-8")

for file in list_dir:
    filename, ext = file.split(".")
    file_content = ""

    if ext == "txt":
        i_file = open(file, "r", encoding="utf-8")
        i_file.readline() #don't add "text"
        file_content = i_file.read()

        o_file.write(file_content)


