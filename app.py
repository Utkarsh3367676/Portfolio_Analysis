from flask import Flask, request, jsonify
from portfolio import PortfolioProcessor
import config
import os
import json

app = Flask(__name__)

# Path to the local JSON file containing transaction data
LOCAL_JSON_PATH = os.path.join(os.path.dirname(__file__), 'transaction_detail.json')

@app.route('/portfolio', methods=['POST'])
def process_portfolio():
    if request.json:
        data = request.json
    else:
        with open(LOCAL_JSON_PATH, 'r') as file:
            data = json.load(file)

    processor = PortfolioProcessor()
    result = processor.calculate_portfolio(data)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
