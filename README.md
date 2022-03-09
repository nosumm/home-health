# home-health 

Developed with: Python Flask, Jinja2 and HTML, and CSS.  

Hosted on Heroku --> using Heroku Postgres Database 

HEROKU TODO:
User database is not connecting to heroku properly
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

