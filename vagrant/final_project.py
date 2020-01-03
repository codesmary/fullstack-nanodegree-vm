from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

@app.route('/restaurants/JSON')
def restaurantsJSON():
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurants = session.query(Restaurant)
    return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantsMenuJSON(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[m.serialize for m in menu_items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantsMenuItemJSON(restaurant_id, menu_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu_item.serialize)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods = ["GET", "POST"])
def newRestaurant():
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<restaurant_id>/edit', methods = ["GET", "POST"])
def editRestaurant(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ["GET", "POST"])
def deleteRestaurant(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant_id=restaurant_id, menu_items=menu_items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ["GET", "POST"])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    if request.method == 'POST':
        new_restaurant = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('showMenu'))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menu_item.name = request.form['name']
        session.add(menu_item)
        session.commit()
        return redirect(url_for('showMenu'))
    else:
        return render_template('editMenuItem.html', menu_item=menu_item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        return redirect(url_for('showMenu'))
    else:
        return render_template('deleteMenuItem.html', menu_item=menu_item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)