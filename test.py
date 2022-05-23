from urllib.request import urlopen
from lxml.html import parse
from encodings.aliases import aliases

youtube_url = 'https://www.youtube.com/watch?v='
url = youtube_url + 'J6XqykqWzbE'
page = urlopen(url)
p = parse(page)


#filename = ("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in "<>:\"/\\|?*"), p.find(".//title").text.replace(" - YouTube", "").replace("【","["))))).replace(" ", "_")
#print(filename)

print(p.find(".//title").text.encode("unicode_escape"))

#from encodings.aliases import aliases
#
#for k in aliases.keys():
#    try:
#        print(k, p.find(".//title").text.encode(k))
#    except:
#        print(k, "impossible")
#
#print("".join(list(filter(lambda ch: ord(ch) > 0 and ord(ch) < 127, p.find(".//title").text.replace(" - YouTube", "")))))