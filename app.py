from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# create a database connection
def get_db():
    db = sqlite3.connect('bank.db')
    db.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, owner TEXT, balance REAL)')
    return db

# create a new account
@app.route('/accounts', methods=['POST'])
def create_account():
    db = get_db()
    owner = request.json['owner']
    balance = request.json['balance']
    db.execute('INSERT INTO accounts (owner, balance) VALUES (?, ?)', (owner, balance))
    db.commit()
    return jsonify({'message': 'Account created successfully'})

# deposit money into an account
@app.route('/accounts/<int:id>/deposit', methods=['PUT'])
def deposit(id):
    db = get_db()
    amount = request.json['amount']
    account = db.execute('SELECT * FROM accounts WHERE id = ?', (id,)).fetchone()

    if account is None:
        return jsonify({'message': 'Account not found'}), 404

    _, _, balance = account
    new_balance = balance + amount
    db.execute('UPDATE accounts SET balance = ? WHERE id = ?', (new_balance, id))
    db.commit()

    return jsonify({'message': 'Deposit successful'})

# withdraw money from an account
@app.route('/accounts/<int:id>/withdraw', methods=['PUT'])
def withdraw(id):
    db = get_db()
    amount = request.json['amount']
    account = db.execute('SELECT * FROM accounts WHERE id = ?', (id,)).fetchone()
    _, _, balance = account
    if account is None:
        return jsonify({'message': 'Account not found'}), 404
    if balance < amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    new_balance = balance - amount
    db.execute('UPDATE accounts SET balance = ? WHERE id = ?', (new_balance, id))
    db.commit()
    return jsonify({'message': 'Withdrawal successful'})

# get account details
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    db = get_db()
    account = db.execute('SELECT * FROM accounts WHERE id = ?', (id,)).fetchone()
    account_id, owner, balance = account
    if account is None:
        return jsonify({'message': 'Account not found'}), 404
    print(account)
    return jsonify({'id': account_id, 'owner': owner, 'balance': balance})

if __name__ == '__main__':
    app.run(debug=True)
