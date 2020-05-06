
import requests
from bs4 import BeautifulSoup
import time
from contextlib import closing
import re, os
import threading
import logManager


class download_img(object):
    def __init__(self):
        self.imgServer = 'http://pic.netbian.com'
        self.start_page = self.imgServer + '/4kmeinv'  # 开始页面
        self.imgUrls = []
        self.pageUrls = []
        self.log = logManager('壁纸')

    '''
    获取所有页面地址
    next_url：当前页面地址
    '''
    def get_page_urls(self, next_url=''):
        if next_url == '':
            next_url = self.start_page

        while 1:
            # 保存页面地址
            print('爬取的页面:', next_url, threading.currentThread())
            self.log.info('爬取的页面:', next_url, threading.currentThread())
            self.pageUrls.append(next_url)
            # 爬取下页地址
            req = requests.get(next_url)
            req.encoding = 'gbk'
            soup = BeautifulSoup(req.text, 'lxml')
            # 获取其它页面链接
            next_urls = soup.select('#main > div.page > a')
            # 判断是否还有下一页
            next_url = ''
            for html in next_urls:
                if re.findall('下一页', html.get_text()):
                    next_url = self.imgServer + html.get('href')
            if next_url == '':
                break
    '''
    获取每个图片的下载地址
    page_url: 每页地址
    '''
    def get_img_urls(self, page_url=''):
        if page_url == '':
            page_url = self.start_page
        req = requests.get(page_url)
        req.encoding = 'gbk'
        soup = BeautifulSoup(req.text, 'lxml')
        # 获取页面中每个图片的下载页面链接
        img_page_urls = soup.select('#main > div.slist > ul > li > a')
        for img_page_url in img_page_urls:
            # 获取单个图片下载页面的地址
            download_page_url = self.imgServer + img_page_url.get('href')
            req = requests.get(download_page_url)
            req.encoding = 'gbk'
            # 获取页面中图片的下载地址
            soup = BeautifulSoup(req.text, 'lxml')
            img_urls = soup.select('#img > img')
            # 保存获取到的下载地址
            for img_url in img_urls:
                img_info = {'url': self.imgServer+img_url.get('src'), 'name': img_url.get('alt')}
                print('爬取的图片:', img_info, threading.currentThread())
                self.log.info('爬取的图片:', img_info, threading.currentThread())
                threadLock.acquire()
                self.imgUrls.append(img_info)
                threadLock.release()
            # 模拟访问，间隔1s
            time.sleep(1)

    '''
    下载图片
    img_info: 图片参数
    '''
    def download(self, img_info):
        print('下载图片:', img_info, threading.currentThread())
        self.log.info('下载图片:', img_info, threading.currentThread())
        # 日志存放路径
        img_dir = './imgs'
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        with closing(requests.get(img_info['url'], stream=True, timeout=5)) as data:
            with open(os.path.join(img_dir, '%s.jpg' % img_info['name']), 'ab+') as f:
                for chunk in data.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


class myThread(threading.Thread):
    def __init__(self, threadID, name, func, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        print('开始线程', self.name)
        self.func(self.args)
        print('退出线程', self. name)


threadLock = threading.Lock()

if __name__ == '__main__':

    obje = download_img()

    thread1 = myThread(1, 'Thread-1', obje.get_page_urls, args='')
    thread1.start()
    thread1.join()

    # 少量数据测试，注释即为全部数据，小心磁盘爆炸
    obje.pageUrls = obje.pageUrls[:5]
    # 一次开启9个线程爬取
    count = len(obje.pageUrls)
    if count > 9:
        count = 9
    while count:
        threadID = 1
        threads = []
        for page_url in obje.pageUrls[0:count]:
            thread = myThread(threadID, 'Thread - %d' % threadID, obje.get_img_urls, page_url)
            thread.start()
            threads.append(thread)
            threadID += 1
        for t in threads:
            t.join()    # 等待线程所有线程结束
        # 截取剩下的资源
        obje.pageUrls = obje.pageUrls[count:]
        count = len(obje.pageUrls)
        if count > 9:
            count = 9

    # 少量数据测试，注释即为全部数据，小心磁盘爆炸
    obje.imgUrls = obje.imgUrls[:10]
    count = len(obje.imgUrls)
    if count > 9:
        count = 9
    while count:
        threadID = 1
        threads = []
        for img_info in obje.imgUrls[0:count]:
            thread = myThread(threadID, 'Thread - %d' % threadID, obje.download, img_info)
            thread.start()
            threads.append(thread)
            threadID += 1
        for t in threads:
            t.join()
        # 截取剩下的资源
        obje.imgUrls = obje.imgUrls[count:]
        count = len(obje.imgUrls)
        if count > 9:
            count = 9
