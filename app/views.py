#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-27 20:51:11
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-28 13:58:41
#

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

from app.models import Movie
from app.viewModels import IndexMovie


web = Blueprint('web', __name__)


@web.route('/top250', methods=['GET'])
def top250():
    page = request.args.get('p')
    page = int(page) if page and page.isdigit() and int(page) else 1
    paginate = Movie.query.order_by(Movie.rank).paginate(page=page, per_page=current_app.config['MOVIES_PER_PAGE'])
    movies = [IndexMovie(m) for m in paginate.items]
    return render_template('index.html', movies=movies, paginate=paginate)


@web.route('/movie/<int:mid>', methods=['GET'])
def movie(mid):
    movie = Movie.query.get(mid)
    return render_template('movie.html', movie=movie)
