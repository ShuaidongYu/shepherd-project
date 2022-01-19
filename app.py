from flask import Flask, jsonify, request, render_template
from pathlib import Path
import json
from core import production_calculation
from core import delivery_calculation

app = Flask(__name__)

consumed_milk = 0.0
consumed_skins = 0
previous_day = 0

xml_file = Path.cwd()/'dat'/'herd.xml'
stock_file = Path.cwd()/'dat'/'stock_info.json'
herd_file = Path.cwd()/'dat'/'herd_info.json'

# get home page for our labyak shop
@app.get('/')
@app.get('/home')
def home():
    return render_template('homepage.html')

@app.get('/yak-shop')
def get_yak_shop():
    return render_template('store_intro.html')

@app.get('/yak-shop/stock')
def get_stock():
    return render_template('stock_info.html')

@app.get('/yak-shop/herd')
def get_herd():
    return render_template('herd_info.html')

@app.get('/yak-shop/stock/<int:day>')
def get_stock_info(day):
        production_calculation(day, xml_file, stock_file, herd_file)
        with open(stock_file, 'r') as f:
            stock = json.load(f)
        return jsonify(stock)

@app.get('/yak-shop/herd/<int:day>')
def get_herd_info(day):
        production_calculation(day, xml_file, stock_file, herd_file)
        with open(herd_file, 'r') as f:
            herd = json.load(f)
        return jsonify(herd)

@app.post('/yak-shop/order/<int:day>')
def create_order(day):
    global consumed_milk
    global consumed_skins
    global previous_day

    # Make sure the order requests come in ascending order of time
    if day < previous_day:
        return jsonify ({'error message': 'Order requests must come in ascending order of time!'})
    previous_day = day

    # Get the order information from the user
    request_data = request.get_json()
    customer = request_data["customer"]
    milk_order = request_data["order"].get("milk")
    skins_order = request_data["order"].get("skins")

    # Get the original stock quantity without any orders
    production_calculation(day, xml_file, stock_file, herd_file)
    with open(stock_file, 'r') as f:
        stock = json.load(f)

    # Update the product amount with the previous consumptions
    total_milk = stock.get("milk") - consumed_milk
    total_skins = stock.get("skins") - consumed_skins
    with open(stock_file, 'w') as f:
        json.dump({"milk": total_milk, "skins": total_skins}, f)

    # Calculate the complete and incomplete orders
    delivery, consumed_milk, consumed_skins = \
        delivery_calculation(stock_file, total_milk, total_skins, \
        customer, milk_order, skins_order, consumed_milk, consumed_skins)

    return jsonify(delivery)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

