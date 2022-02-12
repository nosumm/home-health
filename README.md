# home-health - ongoing project. not hosted publically yet 

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate

required installs:

    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install flask-migrate
    pip install flask-login
    pip install bs4 

 flask environment setup:

    These commands are in a .flaskenv file in the root directory:

        export FLASK_APP=website/app
        export FLASK_ENV=development

Run:

    flask shell
to interact with the database. 
In the flask shell run users = User.query.all() to see all users in the database.

--> - Most recent updates:

    - Configured data transfer between the backend of our website and the thingspeak database. 
    
->  There's a function in app.py using urllib.request.urlopen() to grab data from a thingspeak channel. 

    https://docs.python.org/3/library/urllib.request.html
       
->  The data is stored in the body of a Packet (in the SQLite database of users).
    Packets are linked to users through the user's id. Every user has a unique id. 
    Every packet contains a user_id field that will match the id of exactly one user in the database. 
    This is how we will display test data on the appropriate user's profile.
           
->  You can create a new packet by clicking on the "Create New Test" link on the user profile page.

    Every time you create a packet a new chunk of text like this will be printed: 

    User:noahs 	2022-02-12 05:06:09.928424
    test data:
    b'{"channel":{"id":289288,"name":"postingdata","latitude":"0.0","longitude":"0.0","field1":"Field Label 1","field2":"Field Label 2","created_at":"2017-06-18T10:55:21Z","updated_at":"2018-07-18T08:25:10Z","last_entry_id":92},"feeds":[{"created_at":"2021-05-21T16:41:53Z","entry_id":91,"field1":"100","field2":null},{"created_at":"2021-11-10T03:41:41Z","entry_id":92,"field1":"100","field2":null}]}' TEST#0 

    Packets do not reset when you logout. 
    You can delete packets in the database through the flask shell. 
    to do: implement a delete packet button on the website so users can delete test data they don't want anymore.
