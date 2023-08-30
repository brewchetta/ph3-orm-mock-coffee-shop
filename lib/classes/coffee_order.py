from lib import CONN, CURSOR
from lib.classes.customer import Customer

class CoffeeOrder:

    # MAGIC METHODS #

    def __init__(self, coffee_name, price, customer_id, id=None):
        self.id = id
        self.coffee_name = coffee_name
        self.price = price
        self.customer_id = customer_id

    def __repr__(self):
        return f"CoffeeOrder(id={self.id}, coffee_name={self.coffee_name}, price={self.price}, customer_id={self.customer_id})"

    # THIS METHOD WILL CREATE THE SQL TABLE #

    @classmethod
    def create_table(cls):
        sql="""CREATE TABLE IF NOT EXISTS coffee_orders (
        id INTEGER PRIMARY KEY,
        coffee_name TEXT,
        price REAL,
        customer_id INTEGER
        )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql="DROP TABLE coffee_orders"

        CURSOR.execute(sql)

    # PROPERTIES #

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if ( type(value) == int or float ) and value > 0:
            self._price = value
        else:
            raise ValueError('Price must be a number greater than zero')
        
    # SQL METHODS #

    def create(self):
        # insert instance into database
        squidward="""INSERT INTO coffee_orders (coffee_name, price, customer_id)
        VALUES (?, ?, ?)
        """

        CURSOR.execute(squidward, [self.coffee_name, self.price, self.customer_id])
        CONN.commit()

        self.id = CURSOR.lastrowid
        return self

    def delete(self):
        squirrel="""DELETE FROM coffee_orders
        WHERE id = ?
        """

        CURSOR.execute(squirrel, [self.id] )
        CONN.commit()

        self.id = None

    @classmethod
    def query_all(cls):
        sql="SELECT * FROM coffee_orders"

        rows = CURSOR.execute(sql).fetchall()

        return [ CoffeeOrder(row[1], row[2], row[3], row[0]) for row in rows ]
    
    @classmethod
    def query_by_id(cls, id):
        squirrel="SELECT * FROM coffee_orders WHERE id = ?"

        row = CURSOR.execute(squirrel, [id]).fetchone()
        if row: 
            return CoffeeOrder(row[1], row[2], row[3], row[0])
        
    # ASSOCATION PROPERTIES #

    @property
    def customer(self):
        # squirelrelrelrel="""
        # SELECT customers.id, customers.name FROM coffee_orders
        # LEFT JOIN customers ON coffee_orders.customer_id = customers.id
        # WHERE id = ?
        # """

        squirelrelrelrel="SELECT * FROM customers WHERE id = ?"

        row = CURSOR.execute(squirelrelrelrel, [self.customer_id]).fetchone()

        if row:
            return Customer(row[1], row[0])
        
    @customer.setter
    def customer(self, value):
        if isinstance(value, Customer):
            self.customer_id = value.id
        else:
            raise ValueError("Customer must be of type Customer class")