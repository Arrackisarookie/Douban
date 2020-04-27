#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-04-26 21:50:59
# @Last modified by:   Arrack
# @Last Modified time: 2020-04-27 16:50:01
#
import os

from app import create_app
from dotenv import load_dotenv


dotenvPath = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenvPath):
    load_dotenv(dotenvPath)

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
