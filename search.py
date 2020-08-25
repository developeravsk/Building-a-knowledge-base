import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template,request,jsonify,Response
from retrieval import searchData,retrieveDF

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        data =  request.form["search_param"]
        return Response(result,mimetype='application/json')

@app.route('/explore')
def explore():
    result=retrieveDF()
    print(result.shape)
    return result.to_html()

if __name__ == '__main__':
	app.run()