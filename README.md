# home-health - ongoing project. not hosted publically yet 

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate in Linux or my_env\Scripts\activate in Windows

run: flask run -h localhost -p 8000 to launch the website on port 8000

required installs:

    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install flask-migrate
    pip install flask-login
    pip install bs4 
    pip install flask_mail
    pip install python-dotenv
    pip install flask-wtf

 flask environment setup:

    These commands are in a .flaskenv file in the root directory:

        export FLASK_APP=website/app
        export FLASK_ENV=development


In the flask shell run: 'User.query.all()' to see all users in the database.


--> - completed:

    - set up sqlite database to store users and packets. 
        - Packets are linked to users through the user's id. Every user has a unique id. 
        Every packet contains a user_id field that will match the id of exactly one user in the database. 

    - Configured data transfer between the backend of our website and the thingspeak database. 
        
    - Created profile pages for users
        - Created edit profile functionality. Users can edit their profile fields (username, email, DOB, etc).
        - Implemented grab test data button. displays a packet of data containing test results from thingspeak 
        - Implemented delete test buttons

    extra website features completed:

    - Implemented email us redirect on about page 
    - email and DOB validation (used on edit profile and sign up pages)
    
           
->  You can create a new packet by clicking on the "Create New Test" link on the user profile page.

    Every time you create a packet a new chunk of text like this will be printed: 

    User:noahs 	2022-02-12 05:06:09.928424
    test data:
    b'{"channel":{"id":289288,"name":"postingdata","latitude":"0.0","longitude":"0.0","field1":"Field Label 1","field2":"Field Label 2","created_at":"2017-06-18T10:55:21Z","updated_at":"2018-07-18T08:25:10Z","last_entry_id":92},"feeds":[{"created_at":"2021-05-21T16:41:53Z","entry_id":91,"field1":"100","field2":null},{"created_at":"2021-11-10T03:41:41Z","entry_id":92,"field1":"100","field2":null}]}' TEST#0 

Packets do not reset when you logout.


solution to database connection error randomly encountered:

    - delete migrations folder
    - flask db init - creates new migrations folder
    - flask db revision - creates initial revision
        - go into the generated .py file and replace revision identifier if necessary 
    - flask db migrate and flask db upgrade now work properly 
