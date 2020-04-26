#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 16:40:10
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-26 23:59:08
#

from bs4 import BeautifulSoup
import requests

from app.models import db, Movie


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
            movie['quote'] = item.find(class_='quote').text.strip()
            self.movies.append(movie)
            self.urls.append(movie['url'])

    def getMovies(self):
        for i, url in enumerate(self.urls):
            movie = self.getMovie(url)
            self.movies[i].update(movie)
            m = Movie()
            m.setAttrs(self.movies[i])
            print(m.title)
            db.session.add(m)

    def getMovie(self, url):
        movie = {}
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find(id='content')
        subject = content.find(class_='subject')
        info = subject.find(id='info')
        interest = content.find(id='interest_sectl')

        movie['title'] = content.find('h1').find('span').text
        movie['summary'] = ''.join(content.find(id='link-report').select('span')[-2].text.split())
        movie['year'] = content.find(class_='year').text.replace('(', '').replace(')', '')
        movie['imgSrc'] = subject.find('img')['src']
        movie['ratingNum'] = float(interest.find('strong').text)
        movie['participantsNum'] = int(interest.find(class_='rating_sum').find('span').text)
        movie['awards'] = ' / '.join([''.join(ul.text.split()) for ul in content.find(class_='mod').select('ul')])

        info = self._parseInfo(info)
        movie.update(info)

        return movie

    def _parseInfo(self, info):
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
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def run(self):
        self.getMoviesPerPage()
        self.getMovies()
        self.saveMovies()


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run()
