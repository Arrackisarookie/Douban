#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-27 18:07:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 22:28:13
#

import os

from bs4 import BeautifulSoup
import requests


def crawlPrettyHTML():
    ''' 获取格式良好的 HTML 页面'''

    # :rtype: str

    baseUrl = 'https://movie.douban.com/top250'

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/81.0.4044.113 Safari/537.36')
    }
    response = requests.get(baseUrl, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup.prettify()


def saveHTML(html, path):
    with open(path, 'w') as f:
        f.write(html)


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), 'templates/base.html')
    html = crawlPrettyHTML()
    saveHTML(html, path)
