import os
import csv
import sys

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams
from nltk import trigrams
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import FreqDist

main_dir = "./test_chat_logs" #sys.argv[2]

files = os.listdir(main_dir)

def remove_stop_words(text, reg=r"[a-zA-Z0-9]+", case_sensitive=False):
    stop_words = set(stopwords.words('english'))
    
    reg_tokenizer = RegexpTokenizer(reg)
    word_tokens = reg_tokenizer.tokenize(text)

    if case_sensitive:
        filtered_sentence = [w for w in word_tokens if not w in stop_words]   
    else:
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    return (word_tokens, filtered_sentence)


def ngrams_count_joined(text):
    # split the texts into tokens
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)

    frequence_n1 = FreqDist(tokens)
    frequence_n2 = FreqDist(bi_tokens)
    frequence_n3 = FreqDist(tri_tokens)

    count_n1 = [kv_pair for kv_pair in frequence_n1.items()]
    count_n2 = [kv_pair for kv_pair in frequence_n2.items()]
    count_n3 = [kv_pair for kv_pair in frequence_n3.items()]

    count_n1.sort(key=lambda x: x[1], reverse=True)
    count_n2.sort(key=lambda x: x[1], reverse=True)
    count_n3.sort(key=lambda x: x[1], reverse=True)
    
    return (count_n1, count_n2, count_n3)


def ngrams_count(text):
    # split the texts into tokens
    sep_sentences = sent_tokenize(text)
    s_tokens = []
    bi_tokens = []
    tri_tokens = []
    for sentence in sep_sentences:
        tokens = word_tokenize(sentence)
        tokens = [token.lower() for token in tokens if len(token) > 1]
        s_tokens.extend(tokens)
        bi_tokens.extend(list(bigrams(tokens)))
        tri_tokens.extend(list(trigrams(tokens)))

    frequence_n1 = FreqDist(s_tokens)
    frequence_n2 = FreqDist(bi_tokens)
    frequence_n3 = FreqDist(tri_tokens)

    count_n1 = [kv_pair for kv_pair in frequence_n1.items()]
    count_n2 = [kv_pair for kv_pair in frequence_n2.items()]
    count_n3 = [kv_pair for kv_pair in frequence_n3.items()]

    count_n1.sort(key=lambda x: x[1], reverse=True)
    count_n2.sort(key=lambda x: x[1], reverse=True)
    count_n3.sort(key=lambda x: x[1], reverse=True)

    return (count_n1, count_n2, count_n3)

def process_files():
    for file in files:
        if len(file.split(".")) == 3:
            name, video_id, ext = file.split(".")
            if ext == "csv":
                i_file = open(main_dir + "/" + file, "r", encoding="utf-8")
                i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')

                n_header = next(i_csv_file)

                message_index = n_header.index("message")

                buffer = ""
                print("Reading", name, "...")
                for row in i_csv_file:
                    buffer += row[message_index] + "\n"
                print("Buffer size:", len(buffer), "characters")

                clean_txt = remove_stop_words(buffer)

                ng_list = ngrams_count("\n".join(clean_txt[1]))
                out_dir = "./test_chat_logs/processed/"

                for i, ng_n in enumerate(ng_list):
                    of_name = name + ".n" + str(i + 1) +".txt"
                    out_f = open(out_dir + of_name, "w", encoding="utf-8")

                    print("Outfile: ", of_name)

                    for nn in ng_n:
                        print(nn, file=out_f)


                #print("Most common ngrams[1]:", ng1[0:5])
                #print("Most common ngrams[2]:", ng2[0:5])
                #print("Most common ngrams[3]:", ng3[0:5])


def process_ngram_file(file):
    if len(file.split(".")) == 3:
        name, video_id, ext = file.split(".")
        if ext == "csv":
            i_file = open(file, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')

            n_header = next(i_csv_file)

            message_index = n_header.index("message")

            buffer = ""
            print("Reading", name, "...")
            for row in i_csv_file:
                buffer += row[message_index] + "\n"
            print("Buffer size:", len(buffer), "characters")

            clean_txt = remove_stop_words(buffer, reg=r"[a-zA-Z0-9]+|:[a-zA-Z0-9_]+:")
            #clean_txt = remove_stop_words(buffer.replace("_",""))

            ng_list = ngrams_count("\n".join(clean_txt[1]))

            ret_val = [[], [], []]
            
            for i, ng_n in enumerate(ng_list):
                for nn in ng_n:
                    ret_val[i].append(nn)

            return ret_val

def generate_ngram_files(filename):
    name, id, ext = filename.split(".")

    ngram_list = process_ngram_file(filename)

    for i, ng_n in enumerate(ngram_list):
        of_name = name + ".n" + str(i + 1) +".txt"
        out_f = open(of_name, "w", encoding="utf-8")

        for nn in ng_n:
            print(nn, file=out_f)

if __name__ == "__main__":
    #process_files()
    generate_ngram_files("powerwash.-fBlrjLNHuk.csv")
