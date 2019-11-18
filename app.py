from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# Establish Mongo connection via PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Render index.html with data from Mongo
@app.route("/")
def home(): 
	mars_data = mongo.db.mars_data.find_one()
	return render_template("index.html", mars_data=mars_data)

# Present page with button to scrape data
@app.route("/scrape")
def scrape():
	mars_info = scrape_mars.scrape()
	mars_data = mongo.db.mars_data
	mars_data.update({}, mars_info, upsert=True)
	return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True)