from parsel import Selector
from requests import get
from collections import deque
from time import sleep


def download_one_chapter(url: str, index: int):
    response = get(url)
    response.encoding = response.apparent_encoding

    sel = Selector(response.text)
    h1 = sel.css("h1::text")
    content = sel.css("#content::text")
    title = h1.get()
    text = ""
    for line in content.getall():
        text += line.strip() + "\n"

    with open(file=str(index) + title + '.txt', mode='w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(text)


def download_one_book(home: str, pause: int = 0):
    prefix = home.rstrip("index.html")
    response = get(home)
    response.encoding = response.apparent_encoding

    sel = Selector(response.text)
    urls = sel.css("dd > a::attr(href)")

    url_pool = deque([i for i in enumerate(urls.getall())])

    while len(url_pool):
        sleep(pause)
        index, url = url_pool.popleft()
        try:
            download_one_chapter(prefix + url, index=index)
            print("成功下载第%d章，剩余%d章" % (index, len(url_pool)))
        except:
            url_pool.append((index, url))


if __name__ == "__main__":
    flag = True
    print("小说会下载到当前目录，如果你希望将小说下载到文件夹，请新建文件夹并在文件夹中打开本程序。")
    print(r"书趣阁地址：http://www.shuquge.com/")
    print(r"书趣阁斗破苍穹目录页地址：http://www.shuquge.com/txt/83108/index.html")
    while flag:
        home = input("输入书趣阁小说目录页网址>")
        pause = input("输入下载间隔秒数（默认0秒）>")
        try:
            pause = float(pause)
        except:
            print("无法识别间隔秒数，采取默认0秒。")
            pause = 0
        download_one_book(home, pause)
        if input("你还要继续下载其他小说吗？输入‘y’确认，其他键退出。") == "y":
            flag = False
