from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    db = 'cardeals'
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (price, model, make, year, description, users_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(users_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.users_id = users.id;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_cars = []
        for row in results:
            all_cars.append( cls(row) )
        return all_cars

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_recipe(car):
        is_valid = True
        if int(car['price']) < 0:
            is_valid = False
            flash("Price must be greater than 0","car")
        if len(car['model']) < 2:
            is_valid = False
            flash("Car model must be at least 2 characters","car")
        if len(car['make']) < 2:
            is_valid = False
            flash("Car make must be at least 2 characters","car")
        if int(car['year']) < 0:
            is_valid = False
            flash("Year must be greater than 0","car")
        if len(car['description']) < 2:
            is_valid = False
            flash("Description must be at least 2 characters", "car")
        return is_valid
