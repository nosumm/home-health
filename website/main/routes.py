from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from website.auth.forms import LoginForm, SignupForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from datetime import datetime
# add for thingspeak communication
import urllib
from bs4 import BeautifulSoup
import re # for regex
from flask_mail import Mail
from time import time
import jwt
import random
import numpy as np
from datetime import datetime
import json
import csv
import pandas as pd
from pandas import DataFrame
from io import StringIO
from website.models import User, Packet
from website.main import bp
from website.models import people
from website import db

from bokeh.plotting import figure, show,save,output_file, curdoc
from bokeh.layouts import layout
from bokeh.models import Div,ColumnDataSource, DataTable,TableColumn
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import urllib.request
import pandas as pd
from io import StringIO

from datetime import datetime
import numpy as np

# home page for guests (not logged in)
@bp.route('/')
@bp.route('/index_guest')
def index_guest():
    return render_template("main/index_guest.html", title='Home Page')

# this route renders the user profile page 
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()        
    return render_template('main/user.html', user=user, packets=user.packets.all())

# this app route loads the home page 
# you must log in to view the home page 
# right now the home page simply displays a custom greeting for the user
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template("main/index_login.html", title='Home Page')

# route for edit profile form 
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.DOB = form.DOB.data
        current_user.validate_DOB(form.DOB.data)
        current_user.validate_email(form.email.data) 
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.DOB.data = current_user.DOB
    return render_template('main/edit_profile.html', title='Edit Profile',
                           form=form)

# BELOW ARE THE ROUTES THAT GRAB THE USER'S TEST RESULTS 

seen_packets = [] # TODO: make this part of the user class so each user has their own seen packets array. 
# test type dict stores channel id for each test type
test_types = {'EMG': 'https://api.thingspeak.com/channels/1664068/feeds.csv?api_key=NJCHLCB72TL1X017', 'PULSE': 'https://api.thingspeak.com/channels/1649676/feeds.csv?api_key=JLVZFZMPYNBHIU33'}

# route for the grab new test data button on user profile page    
@bp.route('/newtest/<username>')
def newtest(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not new_packet(user, 'PULSE'):
        flash('No New Test Results Available')
    #else:
        #flash('New Test Result was Grabbed') 
    # render user page again with new packet added
    return render_template('main/user.html', user=user, packets=user.packets.all())

# route for the grab new test data button on user profile page    
@bp.route('/newEMGtest/<username>')
def newEMGtest(username):
    user = User.query.filter_by(username=username).first_or_404()
    #new_EMGpacket(user)
    #if not new_EMGpacket(user):
        #flash('No New Test Results Available')
    #else:
        #flash('New Test Result was Grabbed') 
    # render user page again with new packet added
    url = test_types['EMG'] # grab from appropriate channel. each test type will has its own channel
    thingspeak_read = urllib.request.urlopen(url)
    bytes_csv = thingspeak_read.read()
    data=str(bytes_csv,'utf-8')
    thingspeak_data = pd.read_csv(StringIO(data))
    body_df = pd.DataFrame(thingspeak_data)
    cols = [0,2]
    df = body_df[body_df.columns[cols]]
    #df.style.set_properties(subset=cols[1], **{'font-weight': 'bold'})
    #return render_template('user.html', user=user, packets=user.packets.all())
    return render_template('main/EMGtest.html', user=user, data=df.to_html())

# route for delete all tests button
# deletes all packets for the given user
@bp.route('/deletetests/<username>')
def delete_all_tests(username):
    global seen_packets
    user = User.query.filter_by(username=username).first_or_404()
    packets = user.packets.all()
    seen_packets = []
    for p in packets:
        db.session.delete(p)
    db.session.commit()
    return render_template('main/user.html', user=user, packets=user.packets.all()) 
 
# route for delete this test button
@bp.route('/deletetest/<username>/<packet_id>')
def deletetest(username, packet_id):
    user = User.query.filter_by(username=username).first_or_404()
    p = Packet.query.filter_by(id=packet_id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    return render_template('main/user.html', user=user, packets=user.packets.all())

# this function loops through all the rows in the appropriate csv table (Pulse or EMG)
# checks seen_packets for each row's entry id
# if new entry id --> create new packet for the user with the data from this row
# then add this row's entry id to the user's seen_packets array
# otherwise check the next row
# returns false if no new test result was found
def new_packet(user, test_type):
    global seen_packets
    global test_types
    grab = 0
    done = False
    url = test_types[test_type] # grab from appropriate channel. each test type will has its own channel
    thingspeak_read = urllib.request.urlopen(url)
    bytes_csv = thingspeak_read.read()
    data=str(bytes_csv,'utf-8')
    thingspeak_data = pd.read_csv(StringIO(data))
    body_df = pd.DataFrame(thingspeak_data)
    table_length = len(body_df.index)
    # creates new packet for every row in index and adds packet to our packet_queue 
    while grab < table_length and done is False: 
        this_row = thingspeak_data.iloc[grab] 
        entry_id = str(this_row['entry_id']) # save the entry id for this row
        # check seen packets array for this entry_id
        #if entry_id not in seen_packets:
        if entry_id not in seen_packets:
            test_taken = "Date: "+ str(this_row['field4'])+" Time: "+str(this_row['field5'])
            # create a new packet associated for user 
            p = Packet(body=str(this_row['field3']), author=user, test_type=str(this_row['field2']), test_taken=test_taken) # field2 = test_type
            db.session.add(p) # add packet to db
            db.session.commit()
            seen_packets.append(entry_id) # add this entry id to the seen packets array
            user.add_packet(entry_id) # add this entry id to the user's seen packets array 
            done = True
        grab += 1 
    return done

# route for view entire test result 
@bp.route('/open_packet/<username>/<packet_id>')
def open_packet(username, packet_id):
    user = User.query.filter_by(username=username).first_or_404()
    #pulse_data(packet_id)
    return render_template('main/view_test.html', user=user, packet=Packet.query.get(packet_id))

# route for test visualization/chart page
@bp.route('/open_packet/<username>/test_chart')
def test_chart(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/test_chart.html', user=user)

@bp.route('/pulse_data')
def pulse_data(packet_id):
    # Get Data from thingSpeak
    results = urllib.request.urlopen('https://api.thingspeak.com/channels/1649676/feeds.csv?api_key=JLVZFZMPYNBHIU33')
    bytes_csv = results.read()
    data=str(bytes_csv,'utf-8')
    db =pd.read_csv(StringIO(data))
    db=db.rename(columns={'created_at':'created_at','entry_id':'entry_id','field1':'Username','field2':'Sensor Name','field3':'Value','field4':'Date','field5':'Time'})
    db=db.sort_values(by=['entry_id'])
    grab = 0
    done = False
    while grab < 20 and done is False: 
        # verify this is the right packet
        this_row = db.iloc[-grab]
        if packet_id == this_row['entry_id']: # save the entry id for this row
            done = True
        grab += 1
    # Set varaiables
    pulse_reading = this_row['Value'] # Last entry
    #pulse_reading = db.iloc[-1]['Value'] # Last entry
    x_data = db['entry_id'] # Entry numbers
    y_data = db['Value'] # Data values

    # Color map for single pulse data
    color = 'red'
    level = 'Danger'
    
    if(pulse_reading >=54 and pulse_reading<=73):
        color = 'green'
        level = 'Good'
    elif(pulse_reading >=74 and pulse_reading<=84):
        color = 'yellow'
        level = 'Average'
    elif(pulse_reading >=85):
        color = 'red'
        level = 'High'
    else:
        color = 'red'
        level = 'Danger'
    tools = ['hover']

    div = Div(
    text = ("""<h1> {pulse} BPM </h1> {levels} """).format(pulse=pulse_reading,levels =level), width = 700,style={'font-size': '300%','color': color}
    )
    output_file(filename='website/templates/main/pulse/view_.html')
    show(div)
    render_template('pulse/view_.html')
    
@bp.route('/pulse_plot')
def pulse_plot():
    output_file(filename='Pulse_Plot.html',title='Pulse Plot')
    # Get Data from thingSpeak
    results = urllib.request.urlopen('https://api.thingspeak.com/channels/1649676/feeds.csv?api_key=JLVZFZMPYNBHIU33')
    bytes_csv = results.read()
    data=str(bytes_csv,'utf-8')
    db =pd.read_csv(StringIO(data))
    db=db.rename(columns={'created_at':'created_at','entry_id':'entry_id','field1':'Username','field2':'Sensor Name','field3':'Value','field4':'Date','field5':'Time'})
    db=db.sort_values(by=['entry_id'])

    # Set varaiables
    pulse_reading = db.iloc[-1]['Value'] # Last entry
    x_data = db['entry_id'] # Entry numbers
    y_data = db['Value'] # Data values

    # Color map for single pulse data
    color = 'red'
    level = 'Danger'
    
    if(pulse_reading >=54 and pulse_reading<=73):
        color = 'green'
        level = 'Good'
    elif(pulse_reading >=74 and pulse_reading<=84):
        color = 'yellow'
        level = 'Average'
    elif(pulse_reading >=85):
        color = 'red'
        level = 'High'
    else:
        color = 'red'
        level = 'Danger'
    tools = ['hover']

    div = Div(
    text = ("""<h1> {pulse} BPM </h1> {levels} """).format(pulse=pulse_reading,levels =level), width = 700,style={'font-size': '300%','color': color}
    )
    
    plot = figure(plot_width=600,plot_height=500,tools=tools)
    plot.line(x=x_data,y=y_data)
    plot.circle_dot(x=x_data,y=y_data)
    plot.title.text = 'Pulse Trend over Time'

    dates = db['Date'].to_list
    times = db['Time']
    values = db['Value']
    name = db['Sensor Name']
    s = ColumnDataSource(db)
    c = [
        TableColumn(field='Date',title="Date"),
        TableColumn(field='Time',title="Time"),
        TableColumn(field='Sensor Name',title="Sensor Name"),
        TableColumn(field='Value',title="Value")
        ]
    t = DataTable(source = s, columns = c,width=500,height=2000)
    
    ly_out = layout([[div],[plot],[t]])
    output_file(filename='website/templates/main/Pulse_Plot.html')
    show(ly_out)
    return render_template('main/Pulse_Plot.html')


# NOT WORKING
@bp.route('/emg_plot')
def emg_plot():

    count = 0

    read_data()

    # In[3]:

    plot = figure(width = 900, height = 350)
    source = ColumnDataSource(dict(x=[], y=[]))
    plot.line(x='x',y='y',source=source)


    # In[5]:

    lout = layout([plot])
    curdoc.title = "DATA"
    curdoc().add_root(lout)
    curdoc().add_periodic_callback(update,500)
    output_file(filename='website/templates/main/emg_plotter.html')
    show(lout)
    return render_template('/main/emg_plotter.html')
    

    
def update(count):
    print(count)
    emg_data,time_data = read_data()
    temp1 = [time_data[count]]
    temp2 = [emg_data[count]]
    stream_data=dict(x=temp1,y=temp2)
    source.stream(stream_data)
    plot.title.text = 'EMG'
    count = count + 1
    
def read_data():
    results = urllib.request.urlopen('https://api.thingspeak.com/channels/1664068/feeds.csv?api_key=NJCHLCB72TL1X017&results=160')
    bytes_csv = results.read()
    data=str(bytes_csv,'utf-8')
    db =pd.read_csv(StringIO(data))
    db=db.rename(columns={'created_at':'created_at','entry_id':'entry_id','field1':'Data','field2':'Time'})
    db=db.sort_values(by=['entry_id'])

    emg_data=db['Data'].tolist()
    time_data=db['Time'].tolist()
    t_data = time_data[0]
    t_array =[]
    t_array.append(t_data)
    for i in time_data[1:]:
        t_array.append(t_data+i)
        t_data = t_data + i

    return emg_data,t_array
