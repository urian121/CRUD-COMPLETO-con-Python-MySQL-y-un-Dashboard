
from app import app
from flask import request, session, redirect, url_for


@app.errorhandler(404)
def page_not_found(error):
    if 'conectado' in session and request.method == 'GET':
        return redirect(url_for('inicio'))
    else:
        return redirect(url_for('inicio'))
