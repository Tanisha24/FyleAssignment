from flask import Flask, request
from flask import json,jsonify
# from flask_sqlalchemy import SQLAlchemy
from connection import *
import os


app = Flask(__name__)

@app.errorhandler(404)
def handle_bad_request(e):
    return 'bad request!', 404


@app.errorhandler(500)
def handle_server_error(e):
    return 'Internal Server Error!', 500

 # Test route
@app.route("/")
def hello():
    return "Hello World!"

# http://127.0.0.1:5000/bankifsc?ifsc=ABHY0065002
# Requires parameter 'ifsc'
# Fetches Bank details on the basis of IFSC
@app.route("/bankifsc")
def get_bank_from_ifsc():
    try:
        ifsc=request.args.get('ifsc')
        jsonData=getBankFromIfsc(ifsc)
        print(jsonData)
        return jsonify(jsonData)
    except:
        return "Enter valid IFSC"

# http://127.0.0.1:5000/bankcity?bank=ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED&city=MUMBAI
# Requires parameter 'city' and 'bank'
# Fetches Bank details on the basis of bank and city
@app.route("/bankcity")
def get_bank_from_bank_city():
    try:
        city=request.args.get('city')
        bank=request.args.get('bank')
        jsonData=getDetailsFromBankAndCity(bank,city)
        print(jsonData)
        return jsonify(jsonData)
    except:
        return "Enter valid CITY and BANK"

# Fetches banks tabel
@app.route("/banks")
def get_banks():
    jsonData=getAllBanks()
    print(jsonData)
    return jsonify(jsonData)

# Fetches branches tabel
@app.route("/branches")
def get_branches():
    jsonData=getAllBranches()
    print(jsonData)
    return jsonify(jsonData)


if __name__ == '__main__':
    app.run(debug=True)
