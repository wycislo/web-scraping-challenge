# flask app to render html on local machines.
# also will load data to mongo

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


app = Flask(__name__)

# mongo connection string 
# mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false


# Use PyMongo to establish Mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars





if __name__ == "__main__":
    app.run(debug=True)