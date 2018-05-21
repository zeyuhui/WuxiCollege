import os

from flask import Flask, render_template, jsonify, request, redirect, url_for, g, send_from_directory

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_ckeditor import CKEditor, CKEditorField

from sqlite3 import dbapi2 as sqlite3

app = Flask(__name__)
app.secret_key = 'secret string'

ckeditor = CKEditor(app)

class PostForm(FlaskForm):
	t1 = StringField('t1')
	t2 = StringField('t2')
	t3 = StringField('t3')
	body = CKEditorField('Body', validators=[DataRequired()])
	submit = SubmitField('Submit')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/')
def index():
	# db = get_db()
	# cur = db.execute('select t1, t2, t3, body from entries order by id desc')
	# entries = cur.fetchall()
	# print entries
	return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = PostForm()
	if form.validate_on_submit():
		t1 = form.t1.data
		t2 = form.t2.data
		t3 = form.t3.data
		body = form.body.data
		# You may need to store the data in database here
		db = get_db()
		db.execute('insert into entries (t1, t2, t3, body) values (?, ?, ?, ?)',
	               [t1, t2, t3, body])
		db.commit()
		return redirect(url_for('detail', t1=t1, t2=t2, t3=t3))
	return render_template('edit.html', form=form)

@app.route('/detail', methods=['GET', 'POST'])
def detail():
	#print request.args
	t1 = request.args.get('t1')
	t2 = request.args.get('t2')
	t3 = request.args.get('t3')
	print t1, t2, t3
	db = get_db()
	cur = db.execute('select t1, t2, t3, body from entries where t1=? and t2=? and t3=? order by id desc', [t1,t2, t3])
	entries = cur.fetchall()
	if (len(entries) != 0):
		body = entries[0]['body']
		return render_template('detail.html', body=body)
	else:
		return render_template('detail.html')

app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

@app.route('/files/<filename>')
def files(filename):
    path = 'static/'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
@ckeditor.uploader
def upload():
    f = request.files.get('upload')
    f.save(os.path.join('static/', f.filename))
    url = url_for('files', filename=f.filename)
    return url

if __name__ == '__main__':
    app.run(host='0.0.0.0')