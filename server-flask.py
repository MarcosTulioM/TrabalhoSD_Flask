#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from tinydb import Query, TinyDB


app = Flask(__name__)
CORS(app)  # libera requisições externas


#Criando o banco de dados
db = TinyDB('data.json')
User = Query()

# Carrega o index
@app.route("/")
def home_page():
    return render_template("index.html")

#Busca registros por nome
@app.route('/records', methods=['GET'])
def query_records():
    name = request.args.get('name')
    with open('data.json', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record:
                return jsonify(record[0])
        return jsonify({'error': 'data not found'})


#Criar novo registro
@app.route('/records', methods=['POST'])
def create_record():
    record = request.get_json()
    db.insert(record)
    return jsonify(record)

#Atualizar registro
@app.route('/records', methods=['PUT'])
def update_record():
    record = request.get_json()
    updated = db.update({"email": record["email"]}, User.name == record["name"])
    if updated:
        return jsonify(record)
    return jsonify({'error': 'data not found'})

#Apagar registro
@app.route('/records', methods=['DELETE'])
def delete_record():
    record = request.get_json()
    removed = db.remove(User.name == record["name"])
    if removed:
        return jsonify(record)
    return jsonify({'error': 'data not found'})

# Listar todos os registros
@app.route("/records/all", methods=["GET"])
def list_records():
    return jsonify(db.all())

if __name__ == "__main__":
    app.run(debug=True)