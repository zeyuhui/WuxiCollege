# -*- coding: UTF-8 -*-
import os
import time
import hashlib

from flask import Flask, render_template, jsonify, request, redirect, url_for, g, send_from_directory

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_ckeditor import CKEditor, CKEditorField

from sqlite3 import dbapi2 as sqlite3

app = Flask(__name__)
app.config['CKEDITOR_HEIGHT'] = 500
app.secret_key = 'secret string'

ckeditor = CKEditor(app)

t1_list = [u'学院概况', u'专业设置', u'招生就业', u'本科教学', u'学生服务', u'校友天地', u"学院动态"]

t2_list = [
		[
		{'title':u'简介', 'url':"/list?t1=1&t2=1"}, 
		{'title':u'机构设置', 'url':"/list?t1=1&t2=2"}, 
		{'title':u'获奖情况', 'url':"/list?t1=1&t2=3"}
		],
		[
		{'title':u'汽车电子技术专业', 'url':"/list?t1=2&t2=1"}, 
		{'title':u'汽车检测与维修技术专业', 'url':"/list?t1=2&t2=2"}, 
		{'title':u'汽车营销与服务专业', 'url':"/list?t1=2&t2=3"}, 
		{'title':u'汽车运用与维修技术专业', 'url':"/list?t1=2&t2=4"}, 
		{'title':u'汽车制造与装配技术专业', 'url':"/list?t1=2&t2=5"}
		],
		[
		{'title':u'招生信息', 'url':"/list?t1=3&t2=1"}, 
		{'title':u'就业信息', 'url':"/list?t1=3&t2=2"}, 
		{'title':u'现代学徒制', 'url':"/list?t1=3&t2=3"}, 
		{'title':u'校企合作', 'url':"/list?t1=3&t2=4"}
		],
		[
		{'title':u'院校介绍', 'url':"/list?t1=4&t2=1"}, 
		{'title':u'专业设置', 'url':"/list?t1=4&t2=2"}
		],
		[
		{'title':u'学生组织', 'url':"/list?t1=5&t2=1"}, 
		{'title':u'规章制度', 'url':"/list?t1=5&t2=2"}
		],
		[
		{'title':u'优秀毕业生', 'url':"/list?t1=6&t2=1"}
		],
		[
		{'title':u'动态简讯', 'url':"/list?t1=7&t2=1"}
		]
		]

class PostForm(FlaskForm):
	t1 = StringField('t1')
	t2 = StringField('t2')
	t3 = StringField('t3')
	body = CKEditorField('Body', validators=[DataRequired()])
	submit = SubmitField(u'提交文章')

class PostFormDashboard(FlaskForm):
	submit = SubmitField(u'载入条目')

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
	db = get_db()
	cur = db.execute('select * from entries where t1=? and t2=? order by id desc', ['6', '1'])
	entries = cur.fetchall()
	detail_6_head = {"title" : u"空标题", "abstract": u"空摘要" , "url":"#"}
	detail_6_list = [
		{"title" : u"空标题", "url":"#"},
		{"title" : u"空标题", "url":"#"},
		{"title" : u"空标题", "url":"#"},
		{"title" : u"空标题", "url":"#"}
		]
	length = len(entries)
	if (length > 0):
		detail_6_head["title"] = entries[0]["title"]
		detail_6_head["abstract"] = entries[0]["abstract"]
		detail_6_head["url"] = "/detail?t1=6&t2=1&t3=" + entries[0]["t3"]
		if length > 1:
			last = 5 if length >= 5 else length
			for index in range(1, length):
				detail_6_list[index-1]["title"] = entries[index]["title"]
				detail_6_list[index-1]["url"] = "/detail?t1=6&t2=1&t3=" + entries[index]["t3"]
	cur = db.execute('select * from entries where t1=? and t2=? order by id desc', ['7', '1'])
	entries = cur.fetchall()
	detail_7_head = {"title" : u"动态空标题", "abstract": u"动态空摘要" , "url":"#"}
	detail_7_list = [
		{"title" : u"动态空标题", "url":"#"},
		{"title" : u"动态空标题", "url":"#"},
		{"title" : u"动态空标题", "url":"#"},
		{"title" : u"动态空标题", "url":"#"}
		]
	length = len(entries)
	if (length > 0):
		detail_7_head["title"] = entries[0]["title"]
		detail_7_head["abstract"] = entries[0]["abstract"]
		detail_7_head["url"] = "/detail?t1=7&t2=1&t3=" + entries[0]["t3"]
		if length > 1:
			last = 5 if length >= 5 else length
			for index in range(1, length):
				detail_7_list[index-1]["title"] = entries[index]["title"]
				detail_7_list[index-1]["url"] = "/detail?t1=7&t2=1&t3=" + entries[index]["t3"]
	return render_template('index.html',detail_6_head=detail_6_head, detail_6_list=detail_6_list ,detail_7_head=detail_7_head, detail_7_list=detail_7_list )

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	form = PostFormDashboard()
	t1 = request.form.get('select_lv1')
	t2 = request.form.get('select_lv2')
	if not t1:
		t1 = 1
	if not t2:
		t2 = 1
	print t1, t2
	db = get_db()
	cur = db.execute('select * from entries where t1=? and t2=? order by id desc', [t1,t2])
	entries = cur.fetchall()
	return render_template('dashboard.html', form=form, entries=entries, t1_string=t1_list[int(t1)-1], t2_string=t2_list[int(t1)-1][int(t2)-1]['title'])

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	t3 = request.args.get('t3')
	if t3:
		print t3
		db = get_db()
		cur = db.execute('delete from entries where t3=?', [t3])
		db.commit()
	return redirect(url_for('dashboard'))


@app.route('/edit_article', methods=['GET', 'POST'])
def edit_article():
	form = PostForm()
	return render_template('edit.html', form=form)

@app.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
	form = PostForm()
	if form.validate_on_submit():
		t1 = request.form.get('select_lv1')
		t2 = request.form.get('select_lv2')
		title = request.form.get('title')
		abstract = request.form.get('abstract')
		date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		print 'select_lv1:' + t1
		print 'select_lv2:' + t2
		print 'title:' + title
		print 'abstract:' + abstract
		print  date_time
		body = form.body.data		

		hash_md5 = hashlib.md5(date_time)
		t3 = hash_md5.hexdigest()
		# You may need to store the data in database here
		db = get_db()
		db.execute('insert into entries (t1, t2, t3, title, abstract, date_time, body) values (?, ?, ?, ?, ?, ?, ?)',
	               [t1, t2, t3, title, abstract, date_time, body])
		db.commit()
		return redirect(url_for('detail', t1=t1, t2=t2, t3=t3))

@app.route('/detail', methods=['GET', 'POST'])
def detail():
	#print request.args
	t1 = request.args.get('t1')
	t2 = request.args.get('t2')
	t3 = request.args.get('t3')
	print t1, t2, t3
	db = get_db()
	cur = db.execute('select title, abstract, date_time, body from entries where t1=? and t2=? and t3=? order by id desc', [t1,t2, t3])
	entries = cur.fetchall()
	if (len(entries) != 0):
		title = entries[0]['title']
		date_time = entries[0]['date_time']
		body = entries[0]['body']
		return render_template('detail.html', title=title, date_time=date_time,body=body, t1_string=t1_list[int(t1)-1], t2_list=t2_list[int(t1)-1], t2_string=t2_list[int(t1)-1][int(t2)-1]['title'])
	else:
		return render_template('detail.html')

@app.route('/list', methods=['GET', 'POST'])
def list():
	#print request.args
	t1 = request.args.get('t1')
	t2 = request.args.get('t2')
	page = request.args.get('page')
	if page:
		page = int(page)
	else:
		page = 1
	page_pre_url = "/list?t1="+t1 + "&t2=" + t2 + "&page="+ str( (page-1) if page > 1 else page) 
	page_post_url = "/list?t1="+t1 + "&t2=" + t2 + "&page="+ str(page+1) 
	# print t1, t2, t3
	db = get_db()
	cur = db.execute('select * from entries where t1=? and t2=? order by id desc', [t1,t2])
	entries = cur.fetchall()
	length = len(entries)
	if (length ==1):
		return redirect(url_for('detail', t1=t1, t2=t2, t3=entries[0]['t3']))
	detail_list = []
	if (length > 5*(page-1)):
		last = 5* page if (length >= 5* page) else length
		for i in range(5*(page-1), last):
			detail = {}
			detail["title"] = entries[i]["title"]
			detail["abstract"] = entries[i]["abstract"]
			detail["date_time"] = entries[i]["date_time"]
			detail["url"] ="/detail?t1="+t1 + "&t2=" + t2 + "&t3=" + entries[i]["t3"]
			detail_list.append(detail)
	# if (len(entries) != 0):
	# 	body = entries[0]['body']
	# 	return render_template('list.html', body=body)
	# else:
	return render_template('list.html', detail_list=detail_list, page_pre_url=page_pre_url, page_post_url=page_post_url, t1_string=t1_list[int(t1)-1], t2_list=t2_list[int(t1)-1], t2_string=t2_list[int(t1)-1][int(t2)-1]['title'])

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