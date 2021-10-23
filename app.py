# flask app to render html on local machines.
# also will load data to mongo

import os
from flask import Flask, render_template, redirect
import pymongo
import mission_to_mars


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.images

# print(client.list_database_names())

# check if database exists 
dblist = client.list_database_names()
if collection in dblist:
     print('Database exists')


# collection.drop()
# #db.dropdatabase()

# mydict = {"url_name": "https://nasa.gov/mars"}
# x = collection.insert_one(mydict)


@app.route('/')
def index():
    mars = db.images.find_one()
    return render_template("index.html",mars = mars)

@app.route('/scrape')
def scrape():
	mission_to_mars.scrape()
	return redirect('/', code = 302)


if __name__ == "__main__":
    app.run(debug=True)