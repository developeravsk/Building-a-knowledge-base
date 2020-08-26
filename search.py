import warnings
import json
warnings.filterwarnings("ignore")
from flask import Flask, render_template,request,jsonify,Response, redirect, url_for
from retrieval import searchData,retrieveDF

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search/', methods = ['POST'])
def search():
	data =  request.form.get('search_param')
	# return render_template('result.html',result=result)
	return redirect(url_for("result", data=data))

@app.route('/search/<data>')
def result(data):
	result=searchData(data)
	return render_template('result.html',result=result)

@app.route('/explore/')
def explore():
    result=retrieveDF()
    print(result.shape)
    return result.to_html()

if __name__ == '__main__':
	app.run()

