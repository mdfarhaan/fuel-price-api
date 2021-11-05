from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<district>')
def fuelPrice(district):
    price = {"District": district}
    try:
        #Get petrol price
        petrol_url = "https://www.goodreturns.in/petrol-price-in-" + district + ".html"
        petrol_response = requests.get(petrol_url)
        petrol_src = petrol_response.content
        petrol_soup = BeautifulSoup(petrol_src, "html.parser")
        petrol_tr = petrol_soup.find("tr", {"class":"odd_row"})
        petrol_td = petrol_tr.find_all("td")[1]
        
        #Get diesel price
        diesel_url = "https://www.goodreturns.in/diesel-price-in-" + district + ".html"
        diesel_response = requests.get(diesel_url)
        diesel_src = diesel_response.content
        diesel_soup = BeautifulSoup(diesel_src, "html.parser")
        diesel_tr = diesel_soup.find("tr", {"class":"odd_row"})
        diesel_td = diesel_tr.find_all("td")[1]

        price["Petrol"] = petrol_td.text[2:]
        price["Diesel"] = diesel_td.text[2:]
    except :
        price = {"ERROR 404": "Not Found"}
    
    return jsonify(price)

if __name__ == "__main__":
    app.run()