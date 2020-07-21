from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmark"

mongo = PyMongo(app)


@app.route('/')
def index():
    return '''
        <form method="POST" action="/create" enctype="multipart/form-data">
            <input type="text" name="username">
            <input type="submit" class="like" value="bookmark" >
    '''


@app.route('/create', methods=['POST'])
def save():
    if request.method == 'POST':
        mongo.db.bookmark.insert(
            {'username': request.form.get('username')})

        resp = jsonify('user added successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/user/<id>')
def user(id):
    user = mongo.db.bookmark.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp




@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + ' ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp





if __name__ == " __main__":
    app.run(debug=True)
