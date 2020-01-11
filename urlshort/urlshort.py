import json
import os
from datetime import datetime

from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint

bp = Blueprint('urlshort', __name__, template_folder='templates')


@bp.route('/')
def home():
    return render_template('home.html', codes=session)


@bp.route('/shortened', methods=['GET', 'POST'])
def shortened():
    if request.method == 'POST':

        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That code has already been taken. Please change it.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            file = request.files['file']
            full_name = f"{request.form['code']}_{secure_filename(file.filename)}"
            root_dir = os.path.dirname(os.path.abspath(__file__))
            file.save(os.path.join(root_dir, 'static/user_files/' + full_name))
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = datetime.now()
        return render_template('shortened.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_saved_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
            else:
                return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
