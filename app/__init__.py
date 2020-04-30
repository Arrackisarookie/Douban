#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:50:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-30 18:13:00
#

import click
from flask import Flask

from app.models import db
from app.spider import DoubanSpider
from app.suggestion import sug


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')
    app.config.from_pyfile('secure.py')

    register_blueprint(app)
    register_extensions(app)
    register_command(app)

    return app


def register_blueprint(app):
    from app.views import web
    app.register_blueprint(web)


def register_extensions(app):
    db.init_app(app)
    db.create_all(app=app)
    sug.init_app(app)


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            if click.confirm('This operation will DROP ALL TABLES, continue?'):
                db.drop_all()
                click.echo('All tables have been dropped.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def crawl():
        click.echo('Begin to crawl douban top 250 movies...')
        spider = DoubanSpider()
        spider.run()
        click.echo('Done.')
