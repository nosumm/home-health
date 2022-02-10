# home-health

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate

required installs:

    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install flask-migrate
    pip install flask-login

 flask environment setup:

    These commands are in a .flaskenv file in the root directory:

        export FLASK_APP=website/app
        export FLASK_ENV=development

Run:
    flask shell
to interact with the database. 
In the flask shell run users = User.query.all() to see all users in the database.


Next Steps: 

    Configure the communication between the user database and the thingspeak database.
       
    current high level idea of the process: 
    
        1) The thingspeak database will send packets of data to the sqlite user database. 
        Each packet will represent the results of a single test. Every packet sent must contain a user id. This encodes the user attached to the test. 
        
        2) User database will use the user id to link the recieved packet to the appropriate user. 

        3) Each user will have 0-MAXPACKETS number of packets, each containing their unique user id. 

        The user database has a packet table that contains:
             - a unique packet id
             - the body of the packet (test result data)
             - timestamp
             - user_id that links the packet to it's user
             - test_type represents the type of test taken.

        Users are linked to packets in the database through the packet's user_id field. 
        Every packet contains a user_id which will match the unqiue id of some user in the database. 
        
        We will probably use the packet id field to link packets of data received from the thingspeak database to packets in the user database. 