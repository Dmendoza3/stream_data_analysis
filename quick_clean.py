import re

i_file = open("SuperchatsListening_to_the_RADIO~_only_text20220627151454.csv", "r", encoding="utf-8")
o_file = open("clean.csv", "w", encoding="utf-8")

for line in i_file:
    line_clean = re.sub(r':.*:', '', line) #Stickers
    line_clean = line_clean.replace("\n", "") #.replace(".", "").replace(",","").replace('"', "").replace("’","").replace("'","").replace("!")
    line_clean = re.sub(r'[^a-zA-Z\s,-:]', '', line_clean)

    if line_clean == " ":
        line_clean = ""

    if len(line_clean):
        try:
            print(line_clean, file=o_file)
        except:
            print("error parse")