#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:49:33
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 17:54:10
#

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String


db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer, nullable=False)  # 排名
    title = Column(String(64))              # 名称
    type = Column(String(32))               # 类型
    quote = Column(String(128))             # 一句话电影
    ratingNum = Column(Float)               # 评分
    participantsNum = Column(Integer)       # 评论人数
    countryRegion = Column(String(32))      # 国家/地区
    year = Column(String(10))               # 上映年份
    releaseDate = Column(String(128))       # 上映日期
    language = Column(String(64))           # 语言
    director = Column(String(64))           # 导演
    screenwriter = Column(String(128))      # 编剧
    alias = Column(String(256))             # 别名
    stars = Column(String(2048))            # 主演
    duration = Column(String(128))          # 时长
    website = Column(String(128))           # 官方网站
    summary = Column(String(2048))          # 简介
    imdbID = Column(String(16))             # imdb 编号
    imdbUrl = Column(String(128))           # imdb地址
    imgSrc = Column(String(128))            # 图片地址
    awards = Column(String(1024))           # 奖项

    def setAttrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
