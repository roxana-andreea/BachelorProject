# -*- coding: utf-8 -*-

"""
Auth-Token
~~~~~~~~~~

Securing an Eve-powered API with Token based Authentication and
SQLAlchemy.

This snippet by Andrew Mleczko can be used freely for anything
you like. Consider it public domain.
"""

import json
import base64

from flask import request, jsonify
from werkzeug.exceptions import Unauthorized
from models import User


def register_views(app):

    @app.route('/login', methods=['POST'])
    def login(**kwargs):
        """Simple login view that expect to have username
        and password in the request POST. If the username and
        password matches - token is being generated and return.
        """
        data = request.get_json()
        print("data={}".format(data))
        login = data.get('username')
        password = data.get('password')

        if not login or not password:
            raise Unauthorized('Wrong username and/or password.')
        else:
            user = app.data.driver.session.query(User).get(login)
            if user and user.check_password(password):
                token = user.generate_auth_token()
                return jsonify({'token': token.decode('ascii')})
        raise Unauthorized('Wrong username and/or password.')