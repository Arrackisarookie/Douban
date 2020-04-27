#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 16:40:10
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 17:51:13
#

import requests

from bs4 import BeautifulSoup

from app.models import Movie
from app.models import db


# todo: 多线程

class DoubanSpider(object):
    baseUrl = 'https://movie.douban.com/top250'

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/81.0.4044.113 Safari/537.36')
    }

    movies = []
    urls = []

    def getMoviesPerPage(self, start=0):
        ''' 获取一页中各电影的排名，网址和 quote '''

        params = {
            'start': start
        }
        response = requests.get(self.baseUrl, params=params, headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.ol.select('.item')
        for item in items:
            movie = {}
            movie['rank'] = int(item.em.text)
            movie['url'] = item.find('a')['href']
            quote = item.find(class_='quote')
            movie['quote'] = quote.text.strip() if quote else ''
            self.movies.append(movie)
            self.urls.append(movie['url'])

    def getMovies(self):
        ''' 遍历获取 self.urls 中电影 '''

        for i, url in enumerate(self.urls):
            movie = self.getMovie(url)
            self.movies[i].update(movie)
            m = Movie()
            m.setAttrs(self.movies[i])
            print(m.rank, m.title)
            db.session.add(m)

    def getMovie(self, url):
        ''' 获取电影具体信息 '''

        movie = {}
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find(id='content')
        subject = content.find(class_='subject')
        info = subject.find(id='info')
        interest = content.find(id='interest_sectl')

        summary = content.find(id='link-report').select('span')
        summary = summary[-2] if len(summary) > 1 else summary[0]

        movie['title'] = content.find('h1').find('span').text
        movie['summary'] = ''.join(summary.text.split())
        movie['year'] = content.find(class_='year').text.replace('(', '').replace(')', '')
        movie['imgSrc'] = subject.find('img')['src']
        movie['ratingNum'] = float(interest.find('strong').text)
        movie['participantsNum'] = int(interest.find(class_='rating_sum').find('span').text)
        movie['awards'] = ' / '.join([''.join(ul.text.split()) for ul in content.find(class_='mod').select('ul')])

        info = self._parseInfo(info)
        movie.update(info)

        return movie

    def _parseInfo(self, info):
        ''' 解析 info 中的具体信息 '''

        mapping = {
            '导演': 'director', '编剧': 'screenwriter', '主演': 'stars',
            '类型': 'type', '制片国家/地区': 'countryRegion',
            '语言': 'language', '上映日期': 'releaseDate', '片长': 'duration',
            '又名': 'alias', 'IMDb链接': 'imdbID', '官方网站': 'website'
        }
        movie = {}
        content = info.text
        items = list(filter(None, content.split('\n')))
        for item in items:
            try:
                key, value = item.split(': ', 1)
            except ValueError as e:
                key = '官方网站'
                value = info.select('a')[-1]['href']
            finally:
                movie[mapping[key]] = value
        if '官方小站:' in items:
            movie['imdbUrl'] = info.find_all('a')[-2]['href']
            movie['imdbID'] = movie['imdbUrl'].rsplit('/', 1)[-1]
        else:
            movie['imdbUrl'] = info.find_all('a')[-1]['href']
            movie['imdbID'] = movie['imdbUrl'].rsplit('/', 1)[-1]
        return movie

    def saveMovies(self):
        ''' 写入数据库 '''

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def clean(self):
        ''' 清理 '''

        self.movies = []
        self.urls = []

    def run(self):
        ''' 驱动 '''

        for i in range(0, 226, 25):
            self.getMoviesPerPage(start=i)
            self.getMovies()
            self.saveMovies()
            self.clean()


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run()
