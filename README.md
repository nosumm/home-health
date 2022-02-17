# home-health - ongoing project. not hosted publically yet 

before launching the website you must active the python3 environment (my_env):
    
    source my_env/bin/activate in Linux or my_env\Scripts\activate in Windows

run: flask run -h localhost -p 8000 to launch the website on port 8000

### required installs: ####

    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install flask-migrate
    pip install flask-login
    pip install bs4 
    pip install flask_mail
    pip install python-dotenv
    pip install flask-wtf
    pip install pandas
    pip install numpy

 ### flask environment setup: ###

    These commands are in a .flaskenv file in the root directory:

        FLASK_APP=website/app
        FLASK_ENV=developmentMAIL_SERVER=smtp.googlemail.com
        MAIL_PORT=587
        MAIL_USE_TLS=1
        MAIL_USERNAME=<your-gmail-username>
        MAIL_PASSWORD=<your-gmail-password>


### some database commands: ###

    - User.query.all() returns all users in the database.
    - user = User.query.get(user_id) saves the user with given user_id in user
    - user.packets.all() returns all packets assigned to the user
    - Packet.query.get(packet_id) returns packet with given packet_id
    - db.session.add(to_add)
    - db.session.delete(to_delete)
    - db.session.commit() 

### Completed ###

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

    Every time you create a packet a new chunk of text will be printed.


Packets do not reset when you logout.

### How to reset the migrations folder: ###
This was the solution to a database connection error I randomly starting getting when I tried to run the db migrate, upgrade and downgrade commands.

    - delete migrations folder
    - flask db init - creates new migrations folder
    - flask db revision - creates initial revision
        - go into the generated .py file and replace revision identifier if necessary 
    - flask db migrate and flask db upgrade now work properly 
