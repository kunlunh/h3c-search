from flask import Flask
from flask import render_template
from flask import request,jsonify
import sshsearch
from sshsearch import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testAjax', methods=['GET', 'POST'])
def testAjax():
	building = request.form['building']
	mac = request.form['mac']
	if building == 'A1' :
		hostname = '10.1.1.1'
		tag = 'v5'
	elif building == 'A2' :
		hostname = '10.1.1.2'
		tag = 'v5'
	elif building == 'A3' :
		hostname = '10.1.1.3'
		tag = 'v7'
	elif building == 'B1' :
		hostname = '172.16.0.1'
		tag = 'v5'
	elif building == 'B2' :
		hostname = '172.16.0.2'
		tag = 'v7'
	elif building == 'Admin-5f' :
		hostname = '172.20.0.1'
		tag = 'v5'
	res = swsearch(hostname,mac,tag)
	
	return jsonify(result = res)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8010)
