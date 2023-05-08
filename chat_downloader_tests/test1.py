from chat_downloader import ChatDownloader

url = 'https://www.youtube.com/watch?v=_jkBQKlQNVM'
chat = ChatDownloader().get_chat(url, message_groups=['messages', 'superchat'])       # create a generator

jout = open("test.json", "w", encoding="utf-8")
for message in chat:                        # iterate over messages
    print(message["time_in_seconds"], end="\r")
    print(message, file=jout)