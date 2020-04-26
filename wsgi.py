#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:50:59
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-26 21:52:44
#

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
