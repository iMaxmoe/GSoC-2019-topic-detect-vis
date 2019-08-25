from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import json
from datetime import datetime

import aggregate

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
mongo = PyMongo(app)

date = datetime.strptime("2019-08-01", '%Y-%m-%d')

@app.route('/')
def index():
    jsonFile = [doc for doc in mongo.db.byDate.find({ "date": date })][0]
    jsonFile['_id'] = str(jsonFile["_id"])
    jsonFile['date'] = 0 # useless after find
    jsonFile = json.dumps(jsonFile)
    return render_template("index.html", jsonFile = jsonFile)

@app.route('/', methods=['POST'])
def refresh():
    from_date = datetime.strptime(request.form['from'], '%Y-%m-%d')
    to_date = datetime.strptime(request.form['to'], '%Y-%m-%d')
    
    collection_byDate = mongo.db.byDate
    jsonFiles = collection_byDate.find({ "date": { "$gte": from_date,"$lte": to_date } }) # cursor
      
    return render_template("index.html", jsonFile = aggregate.aggregate(jsonFiles))
    
@app.route('/search')
def search():
    return render_template("search.html")
    
@app.route('/search', methods=['POST'])
def search_refresh():
    name = request.form['name']
    name = aggregate.capitalize_name(name)
    collection_byPerson = mongo.db.byPerson
    try:
        jsonFile = collection_byPerson.find({ "name": name })[0]
        return render_template("search.html", name = name, jsonFile = aggregate.select(jsonFile))
    except:
        return render_template("search.html", name = "Not Found")
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
