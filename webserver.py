from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 5 Delete
            if self.path.endswith("/delete"):
                #
                path = self.path.split('/')[2]
                # filter 
                restaurantQuery = session.query(Restaurant).filter_by(id = path).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Are you sure you want to delete %s?</h1>" % restaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'> " % restaurantQuery.id
                #output += "<input name='deleteRestaurantName' type='text' placeholder ='%s' >" % restaurantQuery.name
                output += "<input type='submit' value='Delete'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            # Objective 4 Rename
            if self.path.endswith("/edit"):
                #
                path = self.path.split('/')[2]
                # filter 
                restaurantQuery = session.query(Restaurant).filter_by(id = path).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                #output += path
                #output += restaurantQuery.name
                output += "<h1> %s </h1>" % restaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'> " % restaurantQuery.id
                output += "<input name='renameRestaurantName' type='text' placeholder ='%s' >" % restaurantQuery.name
                output += "<input type='submit' value='Rename'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return
            # Objective 3 Add new Restaurant
            if self.path.endswith("/restaurant/new"):
                #restaurant_name = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'> "
                output += "<input name='newRestaurantName' type='text' placeholder ='New Restaurant Name' >"
                output += "<input type='submit' value='Create'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            # Objective 1 and 2 
            if self.path.endswith("/restaurant"):
                restaurant_name = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '<a href = "/restaurant/new"> Make a new Restaurant Here </a> </br></br>'
                for restaurantname in restaurant_name:
                    output += restaurantname.name
                    output += str(restaurantname.id)
                    id = restaurantname.id
                    output += "</br>"
                    output += '<a href = "/restaurant/%s/edit"> Edit </a>'% id
                    output += "</br>"
                    output += '<a href = "/restaurant/%s/delete"> Delete </a>'% id
                    output += "</br></br>"

                output += "</body></html>"
                print "hi"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # Delete an existing restarant
            if self.path.endswith("/delete"):
                #
                path = self.path.split('/')[2]
                print path
                print "inside_post_edit"
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    restaurantQuery = session.query(Restaurant).filter_by(id = path).one()
                    print restaurantQuery.name

                    # Delete Restaurant
                    #restaurantQuery.name = messagecontent[0]
                    #    print restaurantQuery.name
                    session.delete(restaurantQuery)
                    session.commit()

                    print restaurantQuery
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()



            # Rename an existing restarant
            if self.path.endswith("/edit"):
                #
                path = self.path.split('/')[2]
                print path
                print "inside_post_edit"
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('renameRestaurantName')
                    print messagecontent[0]
                    #path = self.path.split('/')
                    print path
                    restaurantQuery = session.query(Restaurant).filter_by(id = path).one()
                    print restaurantQuery.name

                    if restaurantQuery != []:
                        # Rename Restaurant
                        restaurantQuery.name = messagecontent[0]
                        print restaurantQuery.name
                        session.add(restaurantQuery)
                        session.commit()

                        print restaurantQuery
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()

            # Add a new restaurant
            if self.path.endswith("/restaurant/new"):
                print "insidepost"
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    print messagecontent

                    # create a new Restaurant
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    print newRestaurant
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()