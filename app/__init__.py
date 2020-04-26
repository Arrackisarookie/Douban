#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:50:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-26 22:43:24
#

import click
from flask import Flask

from app.models import db
from app.spider import DoubanSpider


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.config')

    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

    register_command(app)

    return app


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm(
                'This operation will delete the database, '
                'do you want to continue?')
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
