from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/mac')
def mac():
	print request
	return jsonify(result=2)

if __name__ == '__main__':
    app.run(host='0.0.0.0')