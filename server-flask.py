#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # libera requisições externas


# Carrega o index
@app.route("/")
def home_page():
    return render_template("index.html")

#Busca registros
@app.route('/records', methods=['GET'])
def query_records():
    name = request.args.get('name')
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['name'] == str(name):
                return jsonify(record)
        return jsonify({'error': 'data not found'})


#Criar novo registro
@app.route('/records', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    with open('data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

#Atualizar registro
@app.route('/records', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

#Apagar registro
@app.route('/records', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

app.run(debug=True)