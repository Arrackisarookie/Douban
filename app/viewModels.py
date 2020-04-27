#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-27 21:19:10
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 21:55:42
#


class IndexMovie(object):
    def __init__(self, movie):
        self.id = movie.id
        self.rank = movie.rank
        self.title = movie.title.split(' ', 1)[0]
        self.imgSrc = movie.imgSrc.replace('jpg', 'webp')
        self.quote = movie.quote
        self.director = movie.director
        self.year = movie.year
        self.countryRegion = movie.countryRegion
        self.type = movie.type
        self.ratingNum = movie.ratingNum
        self.participantsNum = movie.participantsNum
        self.alias = movie.alias
