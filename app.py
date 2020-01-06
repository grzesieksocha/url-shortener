import json
import os.path
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = 'dsfjksbdilfbsklbdf'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/shortened', methods=['GET', 'POST'])
def shortened():
    if request.method == 'POST':

        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That code has already been taken. Please change it.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            file = request.files['file']
            full_name = f"{request.form['code']}_{secure_filename(file.filename)}"
            file.save('/home/grzesiek/Documents/python/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return render_template('shortened.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
