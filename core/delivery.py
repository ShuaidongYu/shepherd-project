from collections import OrderedDict
import logging
import sqlite3
from sqlite3 import Error


def delivery_calculation(total_milk, total_skins, \
                         customer, milk_order, skins_order) -> tuple:
    """
    The core logic of computing the order infomation.
    It reads the incoming order and returns the successful order info.
    It also create a db file to store the incomplete orders.

    Args:
        total_milk (float): current amount of milk in stock.
        total_skins (int): current amount of skins in stock.
        customer (str): customer name.
        milk_order (float): incoming milk order.
        skins_order (int): incoming skins order.

    Returns:
        response (list): the succesful order information
        consumed_milk_new (float): the amount of milk that is consumed from this order
        consumed_skins_new (int): the amount of skins that is consumed from this order
        incomplete_order (dict): incomplete order
    """
    delivery = OrderedDict()
    incomplete_order = {}
    consumed_milk_new = 0.0
    consumed_skins_new = 0

    if total_milk >= milk_order and total_skins >= skins_order: # both milk and skins enough
        # delivered milk and skins
        delivery["milk"] = milk_order
        delivery["skins"] = skins_order
        # consumed milk and skins
        consumed_milk_new = milk_order
        consumed_skins_new = skins_order
        # order response
        response = [{"Status": 201}, delivery]
    elif total_milk < milk_order and total_skins >= skins_order: # milk not enough but skins enough
        # delivered milk and skins
        delivery["skins"] = skins_order
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["milk"] = milk_order
        #consumed milk and skins
        consumed_skins_new = skins_order
        # order response
        response = [{"Status": 206}, delivery]
    elif total_milk >= milk_order and total_skins < skins_order: # milk enough but skins not enough
        # delivered milk and skins
        delivery["milk"] = milk_order
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["skins"] = skins_order
        # consumed milk and skins
        consumed_milk_new = milk_order
        # order response
        response = [{"Status": 206}, delivery]
    else: # both milk and skins not enough
        # incomplete order
        incomplete_order["customer"] = customer
        incomplete_order["milk"] = milk_order
        incomplete_order["skins"] = skins_order
        response = [{"Status": 404}]

    return response, consumed_milk_new, consumed_skins_new, incomplete_order

def write_db_order(db_path, incomplete_order):
    """Write the unfulfilled orders to a db file for fellow shepherds to take.
    :param db_path: the database file path
    :param incomplete_order: a dictionary that contains all the order information
    """
    if incomplete_order:
        name = incomplete_order.get("customer")
        milk = incomplete_order.get("milk")
        skins = incomplete_order.get("skins")
        _create_sql_order(db_path, name, milk, skins)


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
        logging.error(Error)
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
        logging.error(Error)

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

def _create_sql_order(path, name, milk, skins):
    """ insert an order into the SQLite database
    :param name: name of the customer
    :param milk: milk amount in the order
    :param skins: skins amount in the order
    :return:
    """
    order = (name, milk, skins)
    conn = _create_connection(str(path))
    _create_table(conn)
    _create_order(conn, order)

