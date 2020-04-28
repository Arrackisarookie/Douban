#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-27 18:07:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 22:42:26
#

import os

from bs4 import BeautifulSoup
import requests


def crawlPrettyHTML(url):
    ''' 获取格式良好的 HTML 页面'''

    # :type url: str
    # :rtype: str

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/81.0.4044.113 Safari/537.36')
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup.prettify()


def saveHTML(html, path):
    with open(path, 'w') as f:
        f.write(html)


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/1292052/'
    filename = 'movie.html'
    filename = os.path.join('templates', filename)
    path = os.path.join(os.path.dirname(__file__), filename)
    html = crawlPrettyHTML(url)
    saveHTML(html, path)
