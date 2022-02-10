# home-health

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


Next Steps: 

    Configure the communication between the user database and the thingspeak database.

    current high level idea of the process: 
    
        1) The thingspeak database will send data to the sqlite user database. 
        Each 'packet' of data sent (not sure how thingspeak will send the data) will represent the results of a single test. 
        Every 'packet' will have a unique packet id and a user id. The user id encodes the user attached to the test. 
        Note the user id field is unique to users but not to packets of data. 
        Multiple packets will be using the same user id if a user has multiple packets attached to their account. 
        
        2) Users are linked to packets in the database through the packet's user_id field. 
        Every packet contains a user_id which will match the unqiue id of some user in the database. 


        3) Each user will have 0-MAXPACKETS number of packets, each containing their unique user id. 
        
        We are using MAXPACKETS because we will probably want to control how many tests a user can have saved at a time.
        (A packet represents the results from a test.)

        The user database has a packet table that contains:
             - a unique packet id
             - the body of the packet (test result data) <-------------- data from thingspeak goes here
             - timestamp
             - user_id that links the packet to it's user
             - test_type represents the type of test taken.

        more resources:

            - references for user database communicating with thingspeak
            
            https://pythonforundergradengineers.com/flask-iot-server-setup.html 

            https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html#create-a-non-root-sudo-user

            - flask request object:

            https://tedboy.github.io/flask/generated/generated/flask.Request.html
            
            https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask


