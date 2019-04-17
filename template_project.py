from flask import Flask, render_template ,request ,redirect , url_for ,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/',methods =['GET','POST'])
def newMenuItem(restaurant_id):
    session = DBSession()
    print("newMenuItem")
    print(request.form.get('name',None))
    if request.method == 'POST':
        print("insidepost")
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuItems.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods =['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    print("insideedit")
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    print(editedItem)
    if request.method == 'POST':
        print("editpost")
        if request.form['name']:
            print("nameeditpost")
            print(request.form['name'])
            editedItem.name = request.form['name']
        session.add(editedItem)
        print("add")
        session.commit()
        flash("Menu Item Edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    print("inside_delete")
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    print(deleteItem.name)
    if request.method == 'POST':
        print("deletepost")
        session.delete(deleteItem)
        print(deleteItem)
        session.commit()
        print("commit")
        flash("Menu Item Deleted Successfuly ")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item = deleteItem)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded = False)