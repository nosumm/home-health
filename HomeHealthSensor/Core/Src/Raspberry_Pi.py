# Imports
import serial
import time
import numpy as np
from time import sleep
from datetime import datetime
import time
from pytz import timezone
import pytz
import urllib.request
import requests
import random

# The function that sends the heart rate data to the database. It will also print a
# success message and the "fields" it sends.
def iot(count):
    pst = timezone('America/Los_Angeles')
    time = datetime.now(pst).strftime('%H:%M:%S')
    date = datetime.now().strftime('%m/%d/%Y')
    url = 'https://api.thingspeak.com/update?api_key=Z5GM7TMDURDOB00G&'
    field1 = 'User1'
    field2 = 'Pulse'
    field3 = count
    field4 = date
    field5 = time
    fields = 'field1={0}&field2={1}&field3={2}&field4={3}&field5={4}'.format(field1, field2, field3, field4, field5)
    fullURL = url+fields
    results = urllib.request.urlopen(fullURL)
    print(results)
    print('success')
    print('field1 = {0}, field2 = {1}, field3 = {2}, field4 = {3}, field5 = {4}'.format(field1, field2, field3, field4, field5))

# This is the function that takes in the data_array and time_array for the EMG data, and convert it into the
# correct format. It then calls the send function to send the EMG data to the database.
def vals(data_array,time_array):
    fields=''
    for val,time in zip(data_array,time_array):
        print(time,val)
        fields += "{1},{0},{2}|".format(val,time,time)
    print(fields)
    send(fields)
    return fields

# This function sends the EMG data to the database, and it will print out the data it sends
def send(fields):
    url = "https://api.thingspeak.com/channels/1664068/bulk_update.csv"
    api = "PMMWHPCC9M3PW1S1"
    time_format = "relative"
    dataEncoded = urllib.parse.urlencode({'write_api_key':api,'time_format':time_format,'updates':fields})
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    results = requests.request("POST",url,headers=header,data=dataEncoded)
    print(results.text)

# This parts initializes the timer and all the variables used
conn = serial.Serial('/dev/ttyS0', 115200)
data = 0
start = 0
first_data = 0
second_data = 0
current_type = 0
previous_time = time.perf_counter()
current_time = time.perf_counter()
time_up = False
pst = timezone("America/Los_Angeles")
old_time = datetime.now(pst).astimezone()

# Initialize the data_array and time_array for the EMG Data
data_array = []
time_array = []

while True:
    # Receiving data from the Raspberry Pi and record the time
    data_first = conn.read()
    sleep(0.03)
    data_left = conn.inWaiting()
    current_data = data_first + conn.read(data_left)
    current_time = time.perf_counter()

    # Clear the data and time array during the time that the test is not running
    if current_data[0] == 200:
        previous_time = current_time
    
    if current_data[0] == 201:
        data_array = []
        time_array = []

    # When 17s have been passed, the time_up signal will be set to true
    if current_time - previous_time > 17:
        time_up = True
        previous_time = current_time

    # 100 and 101 are used to differentiate between heartrate and EMG data
    if current_data[0] == 100:
        start = 1
        current_type = 1
    elif current_data[0] == 101:
        start = 1
        current_type = 2

    # We send every data in two pieces, and we need to combine those two pieces
    # together to form a datapoint.
    if start:
        first_data = 1
        start = 0
    elif first_data:
        data = current_data[0]
        first_data = 0
        second_data = 1
    elif second_data:
        second = current_data[0]
        data = data + second * 100
        second_data = 0
        # Heart Rate Data
        if current_type == 1:
            data_array.append(data)
        # EMG Data (We also need to record the time difference)
        if current_type == 2:
            data_array.append(int(data / 4.5))
            new_time = datetime.now(pst).astimezone()
            time_difference = new_time - old_time
            time_difference = int(time_difference.total_seconds()*1000)
            time_array.append(time_difference)
            old_time = new_time

    # When time is up, we need to send out the data
    if time_up:
        # Print out all the raw data collected
        print(data_array)

        # Send heartrate data (Need to convert the analog signal to BPM)
        if current_type == 1:
            current_type = 0
            data_sum = 0
            average = 0
            new_average = 0
            count = 0
            first_time = True
            goal = 40
            last_index = 0

            # Get the initial average of the data
            for i in range(goal):
                data_sum += data_array[i]
            average = data_sum / goal
            
            for index, data_point in enumerate(data_array):
                # Calculate the running average
                if index > goal:
                    average = (average * goal - data_array[index - goal - 1] + data_array[index - 1]) / goal
                    new_average = average + 20
                # If it crosses the average line for the first time since the last recorded datapoint
                # and there have been at least 5 data points since the last recorded datapoint, then
                # record it as a heart rate datapoint.
                if data_point > new_average and first_time and index - last_index > 5:
                    count += 1
                    last_index = index
                    first_time = False
                elif data_point < new_average:
                    first_time = True

            # The number of data points times 4 is the BPM (We are collecting data every 17s)
            count = count * 4
            print(count)    
            data_array = []
            time_array = []
            time_up = False
            iot(count)
            count = 0
        # Send EMG Data
        elif current_type == 2:
            current_type = 0
            vals(data_array, time_array)
            data_array = []
            time_array = []
            time_up = False
