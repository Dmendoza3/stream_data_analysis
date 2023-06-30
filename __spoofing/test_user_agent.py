from fake_useragent import UserAgent

ua = UserAgent()


for x in range(10):
    print(ua.random)