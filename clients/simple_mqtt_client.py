"""
A simple client writing messages from an LoRaWAN application
to CSV
"""
# standard library
import base64
import binascii
from datetime import datetime
import json
import os
# third party
import paho.mqtt.client as mqtt
from dateutil import tz


# TODO implement mqtt connection code dictionary
HOME = os.path.expanduser('~')
CSV_PATH = os.environ.get('CSV_PATH') or 'loradata/lora_data.csv'
MQTT_HOST = os.environ.get('MQTT_HOST') or 'chirpstack.codefornature.org'
CLIENT_USER = os.environ.get('MQTT_CLIENT_USER') or 'downstream_client'
CLIENT_PASSWORD = os.environ.get('MQTT_CLIENT_PASSWORD')
TOPIC = os.environ.get('MQTT_TOPIC') or 'application/5/device/+/event/up'
# this determines the header and the order of values in the csv
HEADER_DICT = (
    'utc', 'local_time', 'app_id', 'app_name', 'deveui', 'dev_name',
    'decoded_data', 'raw_data', 'no_of_gws', 'id_strngst_gw',
    'name_strngst_gw', 'rssi', 'snr')
LOCAL_TZ = os.environ.get('LOCAL_TZ') or 'America/Los Angeles'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


to_tz = tz.gettz(LOCAL_TZ)
csv_path = os.path.join(HOME, CSV_PATH)


class FileContextManager():
    """
    A context manager managing the files to write to
    """

    def __init__(self, path):
        self.path = path
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        if not os.path.isfile(path):
            with open(path, 'w') as handle:
                header_line = ','.join(HEADER_DICT) + '\r\n'
                handle.write(header_line)

    def __enter__(self):
        self.handle = open(self.path, 'a')
        return self.handle

    def __exit__(self, *args):
        self.handle.close()


def get_rx_info(msg):
    rx_info = msg.get('rxInfo') or []
    gw_info = {}
    last_rssi = -300
    for item in rx_info:
         rssi = int(item.get('rssi'))
         if rssi > last_rssi:
            gw_info = item
            last_rssi = rssi
    return {
        'no_of_gws': len(rx_info),
        'name_strngst_gw': gw_info.get('name'),
        'id_strngst_gw': gw_info.get('gatewayID'),
        'rssi': gw_info.get('rssi'),
        'snr': gw_info.get('loRaSNR')}


def hex_decode_data(data):
    return binascii.hexlify(base64.b64decode(data)).decode('utf-8')


def string_decode_data(data):
    return base64.b64decode(data).decode('utf-8') if data else ''


def parse_message(msg_bytes):
    msg = json.loads(msg_bytes)
    decoded_data = string_decode_data(msg.get('data') or '')
    utc = datetime.utcnow()
    utc = utc.replace(tzinfo=tz.gettz('UTC'))
    local_time = utc.astimezone(to_tz)
    ret = get_rx_info(msg)
    ret.update({
        'utc': utc.strftime(TIME_FORMAT),
        'local_time':  local_time.strftime(TIME_FORMAT),
        'app_id': msg.get('applicationID'),
        'app_name': msg.get('applicationName'),
        'deveui':  msg.get('devEUI'),
        'dev_name':  msg.get('deviceName'),
        'raw_data': msg.get('data'),
        'decoded_data': '"' + decoded_data + '"'})
    return ret


def format_csv(dic, headers=HEADER_DICT):
    ret = ','.join([str(dic.get(key)) for key in headers])
    return ret + '\r\n'


def on_connect(client, userdata, flags, rc):
    print('Connected with result code', str(rc))
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    print('Msg received', datetime.utcnow())
    with FileContextManager(csv_path) as file_handle:
        line = format_csv(parse_message(msg.payload))
        file_handle.write(line)


def main():
    client = mqtt.Client()
    client.username_pw_set(CLIENT_USER, password=CLIENT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    main()
