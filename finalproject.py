from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods=['GET'])
@app.route('/restaurants', methods=['GET'])
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
        if request.method == 'POST':
            newRestaurantName = Restaurant(name=request.form['name'])
            session.add(newRestaurantName)
            session.commit()
            flash("New Restaurant Created!")
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('newRestaurant.html')


@app.route('/restaurant/<int:id>/edit', methods=['GET', 'POST'])
def editRestaurant(id):
    editedRestaurant = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Name Changed!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


@app.route('/restaurant/<int:id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET'])
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
        if request.method == 'POST':
            newItem = MenuItem(name=request.form['name'], description=request.form[
                               'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
            session.add(newItem)
            session.commit()
            flash("new menu item created!")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            return render_template('newMenuItem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    #return "This page is for editing menu item %s" % menu_id
    return render_template('editMenuItem.html', restaurant=restaurant, item=item)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id,item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
