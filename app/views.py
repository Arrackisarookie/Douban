#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-27 20:51:11
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-30 17:24:20
#

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request, jsonify, redirect, url_for

from app.models import Movie
from app.viewModels import IndexMovie
from app.suggestion import sug
from app.forms import SearchForm

web = Blueprint('web', __name__)


@web.route('/top250', methods=['GET', 'POST'])
def top250():
    form = SearchForm(request.form)
    if request.method == 'POST':
        searchText = form.searchText.data
        if searchText:
            return redirect(url_for('web.search', q=searchText))

    page = request.args.get('p')
    page = int(page) if page and page.isdigit() and int(page) else 1
    paginate = Movie.query.order_by(Movie.rank).paginate(page=page, per_page=current_app.config['MOVIES_PER_PAGE'])
    movies = [IndexMovie(m) for m in paginate.items]
    return render_template('index.html', movies=movies, paginate=paginate, form=form)


@web.route('/movies/<int:mid>', methods=['GET', 'POST'])
def movie(mid):
    form = SearchForm(request.form)
    if request.method == 'POST':
        searchText = form.searchText.data
        if searchText:
            return redirect(url_for('web.search', q=searchText))

    movie = Movie.query.get(mid)
    return render_template('movie.html', movie=movie, form=form)


@web.route('/suggestion', methods=['GET'])
def suggestion():
    searchText = request.args.get('q')
    if searchText:
        res = sug.searchPrefix(searchText)
    return jsonify(res)


@web.route('/result', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST':
        searchText = form.searchText.data
        if searchText:
            return redirect(url_for('web.search', q=searchText))

    searchText = request.args.get('q')
    query = Movie.title.like(searchText + '%')
    movies = Movie.query.order_by(Movie.rank).filter(query).all()
    return render_template('result.html', form=form, movies=movies)
