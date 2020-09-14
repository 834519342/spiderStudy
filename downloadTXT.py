
import requests
import sys
import time
from bs4 import BeautifulSoup

"""
类说明：下载《笔趣看》网小说《一念永恒》
Parametes:
    无
Returns:
    无
Modify:
    2020-04-24
"""


class downloaderTXT(object):
    def __init__(self):
        self.__server = 'http://www.biqukan.com'
        self.__target = 'http://www.biqukan.com/1_1094/'
        self.names = []     # 存放章节名
        self.urls = []      # 存放章节链接
        self.nums = 0       # 章节数

    '''
    函数说明：获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2020-04-24
    '''
    def get_domnload_url(self):
        req = requests.get(self.__target)
        req.encoding = 'gbk'
        html = req.text
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')
        a = a_bf.find_all('a')
        self.nums = len(a[12:-2])
        for each in a[12:-2]:
            self.names.append(each.string)
            self.urls.append(self.__server + each.get('href'))

    '''
    函数说明：获取章节内容
    Parameters:
        target - 下载链接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2020-04-24
    '''
    @staticmethod
    def get_contents(target):
        req = requests.get(target)
        req.encoding = 'gbk'
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    '''
    函数说明：将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下，小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2020-04-24
    '''
    @staticmethod
    def writer(name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    dl = downloaderTXT()
    dl.get_domnload_url()
    print('开始爬虫下载')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '爬虫数据.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write(" 进度：%.2f%%" % (float(i/dl.nums)*100) + '\r')
        time.sleep(0.01)
    print('进度：100.00%')
