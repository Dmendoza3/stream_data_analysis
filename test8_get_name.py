from urllib.request import urlopen
from lxml.html import parse

youtube_url = 'https://www.youtube.com/watch?v='
video_id = 'mofTFAEAPfg'
url = youtube_url + video_id
page = urlopen(url)
p = parse(page)

print(("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in ".<>:\"/\\|?*"), p.find(".//title").text.replace(" - YouTube", ""))))).replace(" ", "_") + video_id)