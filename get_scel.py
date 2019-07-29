# 导入必要的包
import os
from urllib import parse
import requests as re
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
def get_file_with_chorme(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    driver.quit()
    return None

# 切换工作目录
try:
    os.chdir("./搜狗细胞词库转换txt")
    print("切换工作目录完成...")
except FileNotFoundError:
    print("已经切换到当前工作目录,无需再次操作...")


# 定义函数,获取当前页面所有类别链接
def url_category(url):
    url_list = []
    url_name = []
    try:
        r = re.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', {'class': 'dict_category_list_title'})
        for div in divs:
            url_list.append('https://pinyin.sogou.com' + div.find('a').get('href'))
            url_name.append(div.find('a').get_text())
        print("当前页面抓取成功, 将返回所有一级大类的url和类别名称\n%s" % url)
    except IOError:
        print("发生未知错误, 页面抓取失败请检查页面布局\n%s" % url)
    return url_name, url_list


# 定义函数,获取当前页面所有类别链接
def get_all_page(url):
    time.sleep(1)
    all_url = []
    try:
        r = re.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find('div', {'id': 'dict_page_list'}).find_all('a')
        num = int(divs[-2].get_text())
        std_url = divs[-2].get('href').split('%s' % num)[0]
        all_url = ['https://pinyin.sogou.com%s%s' % (std_url, x) for x in range(1, num)]
        print("当前页面抓取成功, 将返回所有一级大类的所有页面的url抓取完成")
    except IOError:
        print("发生未知错误, 页面抓取失败请检查页面布局\n%s" % url)
    return all_url


# 定义函数,获取当前页面的10个下载链接
def get_dl_url(url):
    dl_url = []
    try:
        r = re.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', {'class': 'dict_dl_btn'})
        for div in divs:
            dl_url.append(div.find('a').get('href'))
        print("当前页面抓取成功, 将返回所有当前页面的10个下载链接")
    except IOError:
        print("发生未知错误, 页面抓取失败请检查页面\n%s" % url)
    return dl_url


# 定义文件下载函数
def get_file(file_ulr, save_path = "./scel"):
    time.sleep(1)
    file_name = parse.unquote(file_ulr).split('name=')[1]
    print("当前正在下载文件%s.scel" % file_name)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }
    try:
        html_str = re.get(file_ulr, headers).content
        with open('%s/%s.scel' % (save_path, file_name), 'wb') as f:
            f.write(html_str)
        print("文件%s.scel下载完成" % file_name)
    except IOError:
        print("文件%s.scel下载失败" % file_name)
    return None


page_url = []
all_dll = []
sg_url = "https://pinyin.sogou.com/dict/"
category_name, category_url = url_category(sg_url)
for i in range(len(category_url)):
    page_url.extend(get_all_page(category_url[i]))
for i in range(len(page_url)):
    all_dll.extend(get_dl_url(page_url[i]))




pool = ThreadPool(8)
results = pool.map(get_file_with_chorme, all_dll)
pool.close()
pool.join()
