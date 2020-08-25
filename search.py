import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template,request,jsonify,Response
from retrieval import searchData

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        data =  request.form["search_param"]
        result=searchData(data)
        return Response(result,mimetype='application/json')

if __name__ == '__main__':
	app.run()