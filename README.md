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

    Configure the communication between the backend of the website and the thingspeak database.
       
    current high level idea of the process: 
    
        1) The thingspeak database will send packets of data to our user database each with a user id. 
        
        2) User database will use the user id to link the recieved packet to the appropriate user. 

        3) Each user will have n number of packets, each containing their unique user id. 

        Packets of data represent test results from a specific test that was taken.
        
        Packets will need:

        - unique user id 
        - a time field to encode the time the test was taken
        - test type field to encode the test that was taken (EMG, heart rate etc)



