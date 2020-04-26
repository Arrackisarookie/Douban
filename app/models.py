#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:49:33
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-26 23:27:14
#

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, String


db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))              # 名称
    rank = Column(Integer, nullable=False)  # 排名
    ratingNum = Column(Float)               # 评分
    participantsNum = Column(Integer)       # 评论人数
    year = Column(String(10))               # 上映年份
    director = Column(String(32))           # 导演
    screenwriter = Column(String(64))       # 编剧
    stars = Column(String(2048))            # 主演
    type = Column(String(32))               # 类型
    countryRegion = Column(String(32))      # 国家/地区
    website = Column(String(128))           # 官方网站
    language = Column(String(64))           # 语言
    releaseDate = Column(String(64))        # 上映日期
    duration = Column(String(64))           # 时长
    alias = Column(String(256))             # 别名
    imdbID = Column(String(16))             # imdb 编号
    imdbUrl = Column(String(128))           # imdb地址
    summary = Column(String(2048))          # 简介
    imgSrc = Column(String(128))            # 图片地址
    awards = Column(String(1024))           # 奖项

    def setAttrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
