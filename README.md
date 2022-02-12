# home-health - ongoing project. not hosted publically yet 

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate

required installs:

    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install flask-migrate
    pip install flask-login
    pip install uwsgi  

 flask environment setup:

    These commands are in a .flaskenv file in the root directory:

        export FLASK_APP=website/app
        export FLASK_ENV=development

Run:

    flask shell
to interact with the database. 
In the flask shell run users = User.query.all() to see all users in the database.


    
->  The backend of our website will grab data from the thingspeak database. 
       
->  The data will be stored in the body of a Packet (in the SQLite database of users).
    Packets are linked to users through the user's id. Every user has a unique id. 
    Every packet contains a user_id field that will match the id of exactly one user in the database. 
    This is how we will display test data on the appropriate user's profile.
           
    ->  Currently, a new packet will be created every time you refresh the profile page. 
            
    You should see 3 lines like this displayed on the user profile page every time the page is refreshed:

        User:<username>
        test data:
        packet0 	2022-02-11 23:49:10.147126

    The packet number increases with every refresh. Packets do not reset when you logout. 

--> Next Steps: 
    
    - Configure the data transfer between the backend of our website and the thingspeak database.

        - Once I figure out how to retrieve data from the thingspeak database, 
        I will store the retrieved data in the body field of packets in the user database.
        The website is already printing packet contents to user profile pages. 