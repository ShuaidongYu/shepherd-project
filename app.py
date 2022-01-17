from flask import Flask, jsonify, request, render_template
from pathlib import Path
from collections import OrderedDict
import json
from core import core

app = Flask(__name__)

stocks = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

consumed_milk = 0.0
consumed_skins = 0

xml_file = Path.home()/'hobby_projects'/'shepherd-project'/'dat'/'herd.xml'
stock_file = Path.home()/'hobby_projects'/'shepherd-project'/'dat'/'stock_info.json'
herd_file = Path.home()/'hobby_projects'/'shepherd-project'/'dat'/'herd_info.json'

# Get home page for our labyak shop
@app.get('/')
@app.get('/home')
def home():
    return render_template('homepage.html')

#get /yak-shop
@app.get('/yak-shop')
def get_yak_shop():
    return render_template('store_intro.html')

#get /yak-shop/stock
@app.get('/yak-shop/stock')
def get_stock():
    return render_template('stock_info.html')

#get /yak-shop/herd
@app.get('/yak-shop/herd')
def get_herd():
    return render_template('herd_info.html')

@app.get('/yak-shop/stock/<int:day>')
def get_stock_info(day):
        core(day, xml_file, stock_file, herd_file)
        with open(stock_file, 'r') as f:
            stock = json.load(f)
        return jsonify(stock)

@app.get('/yak-shop/herd/<int:day>')
def get_herd_info(day):
        core(day, xml_file, stock_file, herd_file)
        with open(herd_file, 'r') as f:
            herd = json.load(f)
        return jsonify(herd)

@app.post('/yak-shop/order/<int:day>')
def create_order(day):
    delivery = OrderedDict()
    global consumed_milk
    global consumed_skins

    # Get the order information from the user
    request_data = request.get_json()
    milk_order = request_data["order"].get("milk")
    skins_order = request_data["order"].get("skins")

    # Get the original stock quantity without any orders
    core(day, xml_file, stock_file, herd_file)
    with open(stock_file, 'r') as f:
        stock = json.load(f)

    # Update the product amount in the json file with the previous orders
    total_milk = stock.get("milk") - consumed_milk
    total_skins = stock.get("skins") - consumed_skins
    with open(stock_file, 'w') as f:
        json.dump({"milk": total_milk, "skins": total_skins}, f)

    # delivery amount calculation
    if total_milk >= milk_order and total_skins >= skins_order: # both milk and skins enough
        delivery["milk"] = milk_order
        delivery["skins"] = skins_order
        consumed_milk += milk_order
        consumed_skins += skins_order
        with open(stock_file, 'w') as f:
            json.dump({"milk": total_milk-milk_order, "skins": total_skins-skins_order}, f)
        return jsonify({"Status": 201}, delivery)
    elif total_milk < milk_order and total_skins >= skins_order: # milk not enough but skins enough
        delivery["skins"] = skins_order
        consumed_skins += skins_order
        with open(stock_file, 'w') as f:
            json.dump({"milk": total_milk, "skins": total_skins-skins_order}, f)
        return jsonify({"Status": 206}, delivery)
    elif total_milk >= milk_order and total_skins < skins_order: # milk enough but skins not enough
        delivery["milk"] = milk_order
        consumed_milk += milk_order
        with open(stock_file, 'w') as f:
            json.dump({"milk": total_milk-milk_order, "skins": total_skins}, f)
        return jsonify({"Status": 206}, delivery)
    else: # both milk and skins not enough
        return jsonify({"Status": 404})

    # for stock in stocks:
    #     if stock['name'] == day:
    #         new_item = {
    #             'name': request_data['name'],
    #             'price': request_data['price']
    #         }
    #         stock['items'].append(new_item)
    #         return jsonify(new_item)
    # return jsonify ({'message' :'stock not found'})

# #post /yak-shop data: {name :}
# @app.post('/yak-shop/order')
# def create_order():
#     request_data = request.get_json()
#     new_store = {
#       'name':request_data['name'],
#       'items':[]
#     }
#     stocks.append(new_store)
#     return jsonify(new_store)

# #post /yak-shop/<name> data: {name :}
# @app.post('yak-shop/order/<int:day>')
# def create_order(day):
#     request_data = request.get_json()
#     for stock in stocks:
#         if stock['name'] == day:
#             new_item = {
#                 'name': request_data['name'],
#                 'price': request_data['price']
#             }
#             stock['items'].append(new_item)
#             return jsonify(new_item)
#     return jsonify ({'message' :'stock not found'})

#get /yak-shop/<name>/item data: {name :}
# @app.get('/yak-shop/<string:name>/item')
# def get_item_in_store(name):
#     for stock in stocks:
#         if stock['name'] == name:
#             return jsonify( {'items':stock['items'] } )
#     return jsonify ({'message':'stock not found'})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

