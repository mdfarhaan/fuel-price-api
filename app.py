from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup,NavigableString, Comment

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<district>')
def fuelPrice(district):
    price = {"District": district}
    # try:
        #Get petrol price
    petrol_url = "https://www.goodreturns.in/petrol-price-in-" + district + ".html"
    petrol_response = requests.get(petrol_url)
    petrol_src = petrol_response.content
    petrol_soup = BeautifulSoup(petrol_src, "html.parser")
    petrol_block = str(petrol_soup.find("div", {"class":"fuel-block-details"})) 
    petrol_price = ""   
    for i in range(len((petrol_block))) :
        if petrol_block[i].isdigit():
            petrol_price += petrol_block[i]
        elif petrol_block[i] == "." :
            petrol_price += petrol_block[i]
    
    #Get diesel price
    diesel_url = "https://www.goodreturns.in/diesel-price-in-" + district + ".html"
    diesel_response = requests.get(diesel_url)
    diesel_src = diesel_response.content
    diesel_soup = BeautifulSoup(diesel_src, "html.parser")
    diesel_block = str(diesel_soup.find("div", {"class":"fuel-block-details"})) 
    diesel_price = ""   
    for i in range(len((diesel_block))) :
        if diesel_block[i].isdigit():
            diesel_price += diesel_block[i]
        elif diesel_block[i] == "." :
            diesel_price += diesel_block[i]

    price["Petrol"] = petrol_price
    price["Diesel"] = diesel_price
    # except :
    #     price = {"ERROR 404": "Not Found"}
    
    return jsonify(price)

if __name__ == "__main__":
    app.run()