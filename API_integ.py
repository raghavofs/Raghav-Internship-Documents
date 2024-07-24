# API_Integ.py

from flask import Flask, request, jsonify
from bankClass import Bank

app = Flask(__name__)
bank = Bank()

@app.route('/add_account', methods=['POST'])
def add_account():
    data = request.json
    accno = data['accno']
    balance = data.get('balance', 0.0)
    bank.add_account(accno, balance)
    return jsonify({"message": f"Account {accno} added with balance {balance}"}), 200

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    accno = data['accno']
    amount = data['amount']
    result = bank.deposit(accno, amount)
    return jsonify({"message": result}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    accno = data['accno']
    amount = data['amount']
    result = bank.withdraw(accno, amount)
    return jsonify({"message": result}), 200

@app.route('/get_balance/<accno>', methods=['GET'])
def get_balance(accno):
    balance = bank.get_balance(accno)
    return jsonify({"balance": balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
