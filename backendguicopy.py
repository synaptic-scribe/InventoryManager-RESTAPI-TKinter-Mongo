from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from pymongo import MongoClient
from bson import ObjectId
import os 

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory']
products_collection = db['products']

@app.route('/products', methods=['GET'])
def get_products():
    products_list = []
    for product in products_collection.find():
        product.pop('_id',None)
        products_list.append(product)
    return jsonify(products_list), 200

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    pid = str(uuid.uuid4())
    product = {
        'id':pid,
        'name':data['name'],
        'quantity':data['quantity'],
        'price':data['price'],
        'category':data['category']
    }
    products_collection.insert_one(product)
    return jsonify(product),201


@app.route('/products/<pid>', methods=['DELETE'])
def delete_product(pid):
    result = products_collection.delete_one({'id':pid})
    if result.deleted_count > 0:
        return '', 204
    return jsonify({'error':'product not found'}),404

if __name__=='__main__':
    app.run(debug=True)
