from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/chat', methods=('GET', 'POST'))
def chat():

    db = get_db()
    posts = db.execute(
        'SELECT p.id, author_id, msg, created, u.username'
        ' FROM post p JOIN user u'
        ' ON u.id = p.author_id'
        #' WHERE (p.author_id = ? AND p.interlocutor_id = ?)'
        #' OR'
        #' (p.interlocutor_id = ? AND p.author_id = ?)'
        ' ORDER BY p.created DESC',
        #(main_id, user_id, main_id, user_id,)
    ).fetchall()
    pst = {}
    for i in posts:
        pst[i['id']] = [i['username'], i['msg'], i['author_id']]
    dc = pst
    dc = json.dumps(dc)
    return dc


@bp.route('/create/<main_id>', methods=('GET', 'POST'))
def create(main_id):
    if request.method == 'POST':
        msg = request.get_json().get('message')
        error = None

        if not msg:
            error = 'Message is required.'

        if error is not None:
            dc = {'error': error, 'status': 'not'}
            dc = json.dumps(dc)
            return dc
        else:
            db = get_db()
            author_id = main_id
            db.execute(
                'INSERT INTO post (msg, author_id)'
                ' VALUES (?, ?)',
                (msg, author_id)
            )
            db.commit()

            dc = {'success_msg': 'The message successfully sent', 'status': 'ok'}
            dc = json.dumps(dc)
            return dc

    return dc

