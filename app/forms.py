#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-30 16:56:55
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-30 17:12:32
#

from wtforms import Form, StringField


class SearchForm(Form):
    searchText = StringField()
