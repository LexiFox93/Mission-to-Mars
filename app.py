import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars_stuff

# Set route
@app.route("/")
def index():
    mars = client.db.mars_stuff.find()
    #print(mars_stuff)

    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    #mars = client.db.mars
    mars_data = scrape_mars.scrape()
    #mars.update({}, mars_data)
    return "mars data"
    

if __name__ == "__main__":
    app.run(debug=True)