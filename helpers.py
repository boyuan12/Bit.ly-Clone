import random
import string

from functools import wraps
from flask import request, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login')) # , next=request.url
        return f(*args, **kwargs)
    return decorated_function


def random_str(digit=7):
    chars = ""
    for i in range(digit):
        chars += random.choice(string.ascii_letters + string.digits)
    return chars