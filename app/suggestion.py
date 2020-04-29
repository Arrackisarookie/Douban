#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-28 14:37:34
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-29 19:46:09
#

from pytrie import StringTrie


class Suggestion(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def getMovies(self):
        from app.models import Movie
        movies = Movie.query.order_by(Movie.rank).all()
        return movies

    def searchPrefix(self, prefix):
        return self.trie.values(prefix=prefix)

    def parseMovies(self):
        movies = {}
        for movie in self.movies:
            key, value = self.parseMovie(movie)
            movies[key] = value
        return movies

    def parseMovie(self, movie):
        title = movie.title.split(' ', 1)[0]
        rank = movie.rank

        return title, (title, rank)

    def init_app(self, app):
        with app.app_context():
            self.movies = self.getMovies()
        self.moviesDict = self.parseMovies()
        self.trie = StringTrie(self.moviesDict)


sug = Suggestion()
