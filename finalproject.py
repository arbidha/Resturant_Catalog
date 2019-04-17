from flask import Flask, render_template ,request ,redirect , url_for ,flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
#items ={}
#items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','#' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Function shows all my restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurant():
    restaurants = session.query(Restaurant)
    #items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    #return "This page will shows all my restaurants" 
    return render_template('restaurant.html', restaurants = restaurants)

@app.route('/restaurant/new/',methods =['GET','POST'])
def newRestaurant():
    print("Inside new resturatn")
    if request.method == 'POST':
        print("insidepost")
        if request.form['name']:
            print("nameeditpost")
            print(request.form['name'])
            newresturant = Restaurant(name = request.form['name'])
            session.add(newresturant)
            session.commit()
            flash("New Restuarant Created")
            print(newresturant)
            return redirect(url_for('showRestaurant'))
    else:
        return render_template('newrestaurant.html')
    #return "This page will be for making a new restaurant" 
    

@app.route('/restaurant/<int:restaurant_id>/edit/',methods =['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print(editedRestaurant)
    print("Edited")
    print(request.method)
    if request.method == 'POST':
        print("editpost")
        if request.form['name']:
            print("nameeditpost")
            print(request.form['name'])
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        print("add")
        session.commit()
        flash("Restaurant Edited Successfuly")
        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:
        return render_template('editrestaurant.html', restaurant_id = restaurant_id, item = editedRestaurant)
  #return "This page will be for editing restaurant  %s" % restaurant_id
    #return render_template('editrestaurant.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete/',methods =['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print(deletedRestaurant)
    print("Delete")
    print(request.method)
    if request.method == 'POST':
        print("deletepost")
        session.delete(deletedRestaurant)
        print(deletedRestaurant)
        session.commit()
        print("commit")
        flash("Menu Item Deleted Successfuly ")
        return redirect(url_for('showRestaurant'))
    else:
        #return "This page will be for deleting restaurant  %s" % restaurant_id
        return render_template('deleterestaurant.html', restaurant_id = restaurant_id , item = deletedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by (restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/',methods =['GET','POST'])
def newMenuItem(restaurant_id):
    print("Inside new menu")
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)           
        session.add(newItem)
        session.commit()
        flash("New Menu Created")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    #return "This page is for making new menu item for restaurant %s " % restaurant_id  
    

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',methods =['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    print(editedItem)
    print("Edited")
    print(request.method)
    if (request.method == 'POST'):
        print("editpost")
        if request.form['name']:
            print("nameeditpost")
            print(request.form['name'])
            editedItem.name = request.form['name']
        session.add(editedItem)
        print("add")
        session.commit()
        flash("Menu Item Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id ,menu_id = menu_id , item = editedItem )

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',methods =['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id ):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    print(deletedItem)
    print("Delete")
    print(request.method)
    if request.method == 'POST':
        print("deletepost")
        session.delete(deletedItem)
        print(deletedItem)
        session.commit()
        print("commit")
        flash("Menu Item Deleted Successfuly ")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
    #return "This page will be for deleting menu item %s" % menu_id 
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id ,menu_id = menu_id , item = deletedItem )

#
@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(restaurant = [r.serialize for r in restaurant ])


#Making An API Endpoint (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems = [i.serialize for i in items ])

#ADD JSON API ENDPOINT HERE

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
    items = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = items.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded = False)
