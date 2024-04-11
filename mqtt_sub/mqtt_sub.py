#!/usr/bin/env python3

import random
import uuid
import re
import psycopg2 

from paho.mqtt import client as mqtt_client
from config import load_config


# Protocol is MQTT 3.1.1
broker = 'broker.emqx.io' # there are another public MQTT brokers out there!
port = 1883               # You can use http://mqttx.app client to test it

my_id = str(uuid.uuid4()).split('-')[0]  # warn: the topic will change on each run!
topic = f"alhona/fakefactory/{my_id}"

# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'  # Client ids MUST be unique!
username = 'emqx'
password = 'public'

# Initialize empty dictionary
dictionary = {}

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker at {broker}:{port}")
        else:
            print("Failed to connect, return code %d\n", rc)

    _client = mqtt_client.Client(client_id=client_id)
    _client.username_pw_set(username, password)
    _client.on_connect = on_connect
    _client.connect(broker, port)
    return _client

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def subscribe(_client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        processMessage(msg.payload.decode())
        
    print(f"Subscribed to topic {topic}\n")
    _client.subscribe(topic)
    _client.on_message = on_message

def processMessage(message):

    key = re.split("\"*\"", message)
    regex = "^[A-Za-z].*[0-9]$"
    count = 0

    for signal in key:
        if re.match(regex, signal):
            insertDB(signal)
            #getDBFull(signal)


def insertDB(signal):
    """ Retrieve data from the vendors table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT concurrence FROM payload WHERE signal = '"+signal+"'")
                row = cur.fetchone()
                if row is not None:
                    concurrence = int(row[0])
                    concurrence += 1
                    cur.execute("UPDATE payload SET concurrence = "+str(concurrence)+" WHERE signal = '"+signal+"';")
                else:
                    concurrence = 1
                    cur.execute("INSERT INTO payload VALUES(default,'"+signal+"',"+str(concurrence)+");")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 

# Shows Postgres Table Payload for debugging purposes

#def getDBFull(signal):
#    config  = load_config()
#    try:
#        with psycopg2.connect(**config) as conn:
#            with conn.cursor() as cur:
#                cur.execute("SELECT * FROM payload")
#                row = cur.fetchone()
#                print ("\n")
#                while row is not None:
#                    print (row)
#                    row = cur.fetchone()
#
#    except (Exception, psycopg2.DatabaseError) as error:
#        print(error)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()