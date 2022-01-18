from collections import OrderedDict
from pathlib import Path
import json
import sqlite3
from sqlite3 import Error


def _create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error:
        print(Error)
    return conn

def _create_table(conn):
    """ create a table if the table does not exit
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS orders (
                customer TEXT,
                milk REAL,
                skins INTEGER
            )""")
    except Error:
        print(Error)

def _create_order(conn, order):
    """
    Create a new order into the orders table
    :param conn:
    :param order:
    :return:
    """
    sql = ''' INSERT INTO orders(customer, milk, skins)
              VALUES(?,?,?) '''
    c = conn.cursor()
    c.execute(sql, order)
    conn.commit()
    conn.close()

def _create_sql_orders(name, milk, skins):
    """ insert an order into the SQLite database
    :param name: name of the customer
    :param milk: milk amount in the order
    :param skins: skins amount in the order
    :return:
    """
    file_path = Path.home()/'hobby_projects'/'shepherd-project'/'dat'/'orders.db'
    order = (name, milk, skins)
    conn = _create_connection(str(file_path))
    _create_table(conn)
    _create_order(conn, order)


def delivery_calculation(stock_file, total_milk, total_skins, \
    customer, milk_order, skins_order, consumed_milk, consumed_skins) -> tuple:
    """
    The core logic of computing the order infomation.
    It reads the incoming order and returns the successful order info.
    It also create a db file to store the incomplete orders.

    Args:
        stock_file (file object): the json file that contains the stock information.
        total_milk (float): current amount of milk in stock.
        total_skins (int): current amount of skins in stock.
        milk_order (float): incoming milk order.
        skins_order (int): incoming skins order.
        consumed_milk (float): consumed milk from previous orders.
        consumed_skins (int): consumed skins from previous orders.
    Returns:
        response (list): the succesful order information
        consumed_milk (float): the amount of milk that is consumed in the order
        consumed_skins (int): the amount of skins that is consumed in the order
    """
    delivery = OrderedDict()
    incomplete_order = {}

    if total_milk >= milk_order and total_skins >= skins_order: # both milk and skins enough
        # delivered milk and skins
        delivery["milk"] = milk_order
        delivery["skins"] = skins_order
        # cumulatively consumed milk and skins
        consumed_milk += milk_order
        consumed_skins += skins_order
        # remained milk and skins
        remained_milk = total_milk - milk_order
        remained_skins = total_skins - skins_order
        # order response
        response = [{"Status": 201}, delivery]
    elif total_milk < milk_order and total_skins >= skins_order: # milk not enough but skins enough
        # delivered milk and skins
        delivery["skins"] = skins_order
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["milk"] = milk_order
        # cumulatively consumed milk and skins
        consumed_skins += skins_order
        # remained milk and skins
        remained_milk = total_milk
        remained_skins = total_skins - skins_order
        # order response
        response = [{"Status": 206}, delivery]
    elif total_milk >= milk_order and total_skins < skins_order: # milk enough but skins not enough
        # delivered milk and skins
        delivery["milk"] = milk_order
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["skins"] = skins_order
        # cumulatively consumed milk and skins
        consumed_milk += milk_order
        # remained milk and skins
        remained_milk = total_milk - milk_order
        remained_skins = total_skins
        # order response
        response = [{"Status": 206}, delivery]
    else: # both milk and skins not enough
        # remained milk and skins
        remained_milk = total_milk
        remained_skins = total_skins
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["milk"] = milk_order
        incomplete_order["skins"] = skins_order
        response = [{"Status": 404}]
    
    with open(stock_file, 'w') as f:
        json.dump({"milk": remained_milk, "skins": remained_skins}, f)

    if incomplete_order:
        name = incomplete_order.get("customer")
        milk = incomplete_order.get("milk")
        skins = incomplete_order.get("skins")
        _create_sql_orders(name, milk, skins)

    return response, consumed_milk, consumed_skins

