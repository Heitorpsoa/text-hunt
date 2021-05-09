import flask
from controller import cont

app = flask.Flask(__name__)

_cont = cont.Controller()

@app.route('/', methods=["GET"])
def home():
    return flask.render_template('home.html')

@app.route('/originals', methods=["GET"])
def originals():
    texts = _cont.getRawTexts()
    return flask.render_template('texts.html', texts = texts)

@app.route('/processed', methods=["GET"])
def processeds():
    texts = _cont.getProcessedTexts()
    return flask.render_template("texts.html", texts = texts)

@app.route('/indexation', methods=["GET"])
def indexation():
    index = _cont.index
    return flask.render_template("indexation.html", index = index)

@app.route('/search', methods=["GET"])
def search():
    tags = _cont.getAllTags()
    return flask.render_template("search.html", tags = tags)

@app.route('/search/go', methods=["POST"])
def searchGo():
    term = flask.request.form['term']
    tags = flask.request.form.getlist('tags')

    result = _cont.search(term, tags)
    return flask.render_template('result.html', result = result, term = term)

@app.route('/search/redirect/<int:documentIndex>/<string:term>', methods=["GET"])
def redirect(documentIndex, term):
    text = _cont.getText(documentIndex)
    return flask.render_template('single-text.html', text=text, term=term) 


app.run('localhost', port=3200, debug=True)