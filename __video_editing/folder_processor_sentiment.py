import os
import csv
#import sys
from file_explorer import folder_iterator
from nltk.sentiment import SentimentIntensityAnalyzer

main_dir = "./test_chat_logs" #sys.argv[2]

files = os.listdir(main_dir)

def sentiment_analysis(text, sia):
    ret_val = sia.polarity_scores(text)
    return ret_val

def process_files():
    sia = SentimentIntensityAnalyzer()

    for file in files:
        if len(file.split(".")) == 3:
            name, video_id, ext = file.split(".")
            if ext == "csv":
                i_file = open(main_dir + "/" + file, "r", encoding="utf-8")
                i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')

                out_dir = "./test_chat_logs/processed/"

                of_name_sa = name + ".sa.txt"
                out_f_sa = open(out_dir + of_name_sa, "w", encoding="utf-8")
                headers_sa = "message,compound,timestamp,elapsedTime"
                print(headers_sa, file=out_f_sa)
                print("Outfile_sa: ", of_name_sa)

                line = 1
                next(i_csv_file)
                for row in i_csv_file:
                    ##sentiment analysis
                    print("line", line, " "*10, end="\r")
                    line += 1
                    compound = sentiment_analysis(row[0], sia)["compound"]
                    print('"' + row[0] + '"', compound, row[1], row[2], sep=",", file=out_f_sa)

def clean_process_files():
    sia = SentimentIntensityAnalyzer()

    for filename, is_directory, full_path in folder_iterator(main_dir, "csv"):
        if len(filename.split(".")) == 3:
            name, video_id, ext = filename.split(".")
            i_file = open(full_path, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')

            out_dir = "./test_chat_logs/processed/"

            of_name_sa = name + ".sa.txt"
            out_f_sa = open(out_dir + of_name_sa, "w", encoding="utf-8")
            headers_sa = "message,compound,timestamp,elapsedTime"
            print(headers_sa, file=out_f_sa)
            print("Outfile_sa: ", of_name_sa)

            line = 1
            next(i_csv_file)
            for row in i_csv_file:
                ##sentiment analysis
                print("line", line, " "*10, end="\r")
                line += 1
                compound = sentiment_analysis(row[0], sia)["compound"]
                print('"' + row[0] + '"', compound, row[1], row[2], sep=",", file=out_f_sa)


if __name__ == "__main__":
    #process_files()
    clean_process_files()
