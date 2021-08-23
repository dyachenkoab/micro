#!env/bin/python3
import pymongo
import json
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import Response


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
mongo = PyMongo(app)

@app.route("/id", methods=['POST'])
def getByID():
    if request.is_json:
        data = request.get_json()
        if data is None or data == {}:
            return Response(json.dumps({'Error': 'No valid data'}),
                            status=400,
                            mimetype='application/json')
    else:
        return Response(json.dumps({'Error': 'Data not in json'}),
                        status=400,
                        mimetype='application/json')

    if '_id' not in data.keys():
        return Response(json.dumps({'Error': 'No ID'}),
                        status=400,
                        mimetype='application/json')

    cursor = mongo.db.inventory.find_one({'_id': data['_id']})
    return Response(json.dumps(cursor),  mimetype='application/json')

@app.route("/add_one", methods=['POST'])
def add_one():
    if request.is_json:
        data = request.get_json()
        if data is None or data == {}:
            return Response(json.dumps({'Error': 'No valid data'}),
                            status=400,
                            mimetype='application/json')
    else:
        return Response(json.dumps({'Error': 'Data not in json'}),
                        status=400,
                        mimetype='application/json')

    for i in ['_id', 'name', 'parameters']:
        if i not in data.keys():
            return Response(json.dumps({'Error': 'Bad value'}),
                            status=400,
                            mimetype='application/json')

    try:
        mongo.db.inventory.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        return Response(json.dumps({'Error':'Duplicated id\'s'}),  mimetype='application/json')

    return Response(json.dumps({'Success':'OK'}),  mimetype='application/json')

@app.route("/filter", methods=['POST'])
def filter():
    pipeline = []
    if request.is_json:
        data = request.get_json()
        if data is None or data == {}:
            return Response(json.dumps({'Error': 'No valid data'}),
                            status=400,
                            mimetype='application/json')
    else:
        return Response(json.dumps({'Error': 'Data not in json'}),
                        status=400,
                        mimetype='application/json')

    for key in data.keys():
        if key == 'name':
            match_name = {'$match':{'name':data['name']}}
            pipeline.append(match_name)
        if key == 'color':
            match_color = {'$match':{'parameters.color':data['color']}}
            pipeline.append(match_color)
        if key == 'part_number' and isinstance(data['part_number'], int):
            match_part_number = {'$match':{'parameters.part_number':data['part_number']}}
            pipeline.append(match_part_number)

    projection = {'$project':{'parameters': 0, 'description': 0}}
    pipeline.append(projection)

    cursor = mongo.db.inventory.aggregate(pipeline)
    res = [i for i in cursor]
    return Response(json.dumps(res),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
