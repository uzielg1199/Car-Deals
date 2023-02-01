from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User


@app.route('/new')
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_car.html',user=User.get_by_id(data))

@app.route('/create/car',methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_recipe(request.form):
        return redirect('/new')
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "users_id": session["user_id"]
    }
    Car.save(data)
    return redirect('/dashboard')

@app.route('/edit/car/<int:id>')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_car.html",edit=Car.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/car',methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_recipe(request.form):
        return redirect('/edit/car/<int:id>')
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "id": request.form['id']
    }
    Car.update(data)
    return redirect('/dashboard')

@app.route('/car/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_car.html",cars=Car.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/car/<int:id>')
def destroy_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.destroy(data)
    return redirect('/dashboard')