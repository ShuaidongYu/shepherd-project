from flask import Flask, jsonify, request, render_template
import os
import json
from core import production_calculation
from core import dump_json_herd
from core import dump_json_stock
from core import delivery_calculation
from core import write_db_order

app = Flask(__name__)

consumed_milk_total = 0.0
consumed_skins_total = 0
previous_day = 0


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

xml_file = os.path.join(ROOT_DIR, 'dat', 'herd.xml')
stock_file = os.path.join(ROOT_DIR, 'dat', 'stock_info.json')
herd_file = os.path.join(ROOT_DIR, 'dat', 'herd_info.json')
db_file = os.path.join(ROOT_DIR, 'dat', 'orders.db')

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
        product_info, _ = production_calculation(day, xml_file)
        dump_json_stock(stock_file, product_info)
        with open(stock_file, 'r') as f:
            stock = json.load(f)
        return jsonify(stock)

@app.get('/yak-shop/herd/<int:day>')
def get_herd_info(day):
        _, herd_info = production_calculation(day, xml_file)
        dump_json_herd(herd_file, herd_info)
        with open(herd_file, 'r') as f:
            herd = json.load(f)
        return jsonify(herd)

@app.post('/yak-shop/order/<int:day>')
def create_order(day):
    global consumed_milk_total
    global consumed_skins_total
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
    product_info, _ = production_calculation(day, xml_file)

    # Update the product amount with the previous consumptions
    total_milk = product_info.get("milk") - consumed_milk_total
    total_skins = product_info.get("skins") - consumed_skins_total

    # Calculate the complete and incomplete orders
    delivery, consumed_milk_new, consumed_skins_new, incomplete_order = \
    delivery_calculation(total_milk, total_skins, \
                        customer, milk_order, skins_order)

    # Update the stock amount with the new order
    with open(stock_file, 'w') as f:
        json.dump({"milk": total_milk-consumed_milk_new, "skins": total_skins-consumed_skins_new}, f)

    # Update the recorded total consumptions
    consumed_milk_total += consumed_milk_new
    consumed_skins_total += consumed_skins_new

    # Store the incomplete order to a db file
    write_db_order(db_file, incomplete_order)

    return jsonify(delivery)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

