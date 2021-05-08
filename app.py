import flask
from controller import cont

app = flask.Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return flask.render_template('home.html')

@app.route('/originals', methods=["GET"])
def originals():
    texts = cont.getRawTexts()
    return flask.render_template('texts.html', texts = texts)

@app.route('/processed', methods=["GET"])
def processeds():
    texts = cont.getProcessedTexts()
    return flask.render_template("texts.html", texts = texts)

@app.route('/indexation', methods=["GET"])
def indexation():
    index = cont.indexation()
    return flask.render_template("indexation.html", index = index)

@app.route('/search', methods=["GET"])
def search():
    tags = cont.getAllTags()
    return flask.render_template("search.html", tags = tags)

@app.route('/search/go', methods=["get"])
def searchGo():
    term = flask.request.args.get('term')
    result = cont.search(term)
    return flask.render_template('result.html', result = result, term = term)

@app.route('/search/redirect/<int:documentIndex>/<string:term>', methods=["GET"])
def redirect(documentIndex, term):
    text = cont.getText(documentIndex)
    return flask.render_template('single-text.html', text=text, term=term) 


app.run('localhost', port=3200, debug=True)