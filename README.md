# home-health 

Hardware code: .c files are located HomeHealthSensor/Core/Src and .h files are located in HomeHealthSensor/Core/Inc

Website code: 
All website files are located in the website folder. 
HTML templates are located in website/templates. 
Our CSS file and images are located in website/static. 
website/auth contains all the code that authenticates users during the sign up and log in process on the website. 
website/errors contains the code that handles errors on the website. 
website/about contains the code for our about and home page. 
website/main contains the code that grabs test result data and connects our user accounts db (SQLite) to our sensor data db (Thingspeak). 

Website Developed with: Python Flask, Jinja2 and HTML, and some CSS.  

Hosted on Heroku --> using Heroku Postgres Database 

HEROKU:
User database under maintenance - login and sign up temporarily disabled

https://home-health-station.herokuapp.com/


## Development Notes

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate in Linux or my_env\Scripts\activate in Windows

run: flask run -h localhost -p 8000 to launch the website on port 8000

### some database commands: ###

    - User.query.all() returns all users in the database.
    - user = User.query.get(user_id) saves the user with given user_id in user
    - user.packets.all() returns all packets assigned to the user
    - Packet.query.get(packet_id) returns packet with given packet_id
    - db.session.add(to_add)
    - db.session.delete(to_delete)
    - db.session.commit() 
    
### How to reset the migrations folder: ###
This was the solution to a database connection error I randomly starting getting when I tried to run the db migrate, upgrade and downgrade commands.

    - delete migrations folder
    - flask db init - creates new migrations folder
    - flask db revision - creates initial revision
    - try to run flask db migrate
        - you will probably get an error like this:
        Error: Can't locate revision identified by '<some_id>'
        - go into the generated .py file in migrations/versions/__pycache__ and replace revision id with the id from error message
    - flask db migrate and flask db upgrade now work properly 

