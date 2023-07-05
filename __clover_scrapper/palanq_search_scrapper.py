from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from urllib.parse import urlparse
import time
import random

ua = UserAgent()

def get_urls(search_phrase, board="vt", page=1, min_post=1, date_start="", date_end=""):
    url = lambda page, start, end : f"https://archive.palanq.win/{board}/search/text/{search_phrase}/page/{page}/" + (f"start/{start}/"  if start else "") + (f"end/{end}/" if end else "")

    request = Request(url(page, date_start, date_end))
    user_agent = ua.random
    print("trying", user_agent)
    request.add_header('User-Agent', user_agent)
    search_doc = urlopen(request).read().decode('utf8')

    soup = BeautifulSoup(search_doc, 'html.parser')

    post_section = soup.find(lambda tag: tag.name=='aside')
    if not post_section:
        return []
    
    post_list = post_section.find_all("article", {"class": "post"})

    ret_list = []

    for post in post_list:
        post_id = post["id"]
        parsed_dt = datetime.fromisoformat(post.find("time")["datetime"])
        tag_text = post.find("div", {"class": "text"}).find_all("a")

        if int(post_id) < int(min_post):
            break

        url_list = []
        for link in tag_text:
            p = urlparse(link["href"])
            #scheme,netloc,path,params,query,fragment
            url_list.append(p)
        ret_list.append((post_id, parsed_dt, url_list))


    return ret_list

def find_links_until(search_phrase, page_range=(1,-1), min_post=-1, date_start="", date_end=""):
    max_retries = 5
    retries = 0
    alive = True
    page = page_range[0]

    last_page = -1

    if page_range[0] <= 0:
        page = 1

    if page_range[1] == -1:
        last_page = 99999
    elif page_range[1] < page_range[0]:
        return []

    if min_post == -1:
        min_post = 1

    full_url_list = []
    while alive:
        print("downloading page", page)
        try:
            url_list = get_urls(search_phrase, page=page, min_post=min_post, date_start=date_start, date_end=date_end)
            retries = 0
        except Exception as e:
            retries += 1
            alive = retries < max_retries
            print("retries", retries, "/", max_retries, "error", e)
            continue

        full_url_list.extend(url_list)

        page += 1
        alive = bool(url_list)
        if page > last_page:
            alive = False

        if int(full_url_list[-1][0]) < int(min_post):
            alive = False

        time.sleep(random.randint(4,7))

    full_url_list

    return full_url_list


# def parse_local_html():
#     search_doc = open("raw.html", "r", encoding="utf-8").read()

#     soup = BeautifulSoup(search_doc, 'html.parser')

#     post_list = soup.find(lambda tag: tag.name=='aside').find_all("article", {"class": "post"})

#     ret_list = []

#     for post in post_list:
#         post_id = post["id"]
#         parsed_dt = datetime.fromisoformat(post.find("time")["datetime"])
#         tag_text = post.find("div", {"class": "text"}).find_all("a")
#         url_list = []
#         for link in tag_text:
#             p = urlparse(link["href"])
#             #scheme,netloc,path,params,query,fragment
#             url_list.append(p)
#         ret_list.append((post_id, parsed_dt, url_list))


#     return ret_list


if __name__ == "__main__":
    #urls_list = get_urls("catbox.moe", page=16, date_start="2023-07-03", date_end="2023-07-04")
    urls_list = find_links_until("catbox.moe", page_range=(1, -1), min_post=52718339, date_start="2023-07-03", date_end="2023-07-04")
    out_f = open("group_list.csv", "w", encoding="utf-8")
    out_l_f = open("url_list.csv", "w", encoding="utf-8")
    
    print("post_id,parsed_date,url_count", file=out_f)
    print("netloc,path", file=out_l_f)

    for group in urls_list:
        post_id, parsed_dt, url_list = group
        for parsed_url in url_list:
            scheme,netloc,path,params,query,fragment = parsed_url
            print(netloc, path, sep=",", file=out_l_f)        
        print(post_id, parsed_dt, len(url_list), sep=",", file=out_f)
