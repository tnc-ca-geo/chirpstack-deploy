"""
A simple client writing messages from an LoRaWAN application
to CSV
"""
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print('Connected with result code', str(rc))
    client.subscribe('application/2/device/+/event/up')


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)


client = mqtt.Client()
client.username_pw_set('downstream_client', password='happyL0RA')
client.on_connect = on_connect
client.on_message = on_message
client.connect('chirpstack.codefornature.org', 1883, 60)
client.loop_forever()
