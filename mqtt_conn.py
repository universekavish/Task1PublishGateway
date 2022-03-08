import time,ssl,json,random,sys
import paho.mqtt.client as mqtt
from multiprocessing import Pool
settings = {}
CC = "US"
#target = sys.argv[1]
target = '192.168.247.194'
settings_topic = "gateway/settings"
topic1 = "gateway/events"
scan_list_topic = "gateway/scan_list"

my_topic1 = "gateway/device/authentication"
my_topic2 = "gateway/zigbee/device/settings"
my_topic3 = "gateway/zigbee/device/function/attribute"

ssl_enabled = 'True'
MQTT = {
    "ca_cert": '/home/asm/Downloads/ruckusCertificates/ca.crt',
    "client_crt": "/home/asm/Downloads/ruckusCertificates/ap.crt",
    "client_key": "/home/asm/Downloads/ruckusCertificates/ap.key"
}

ca_file=MQTT.get("ca_cert")
client_crt=MQTT.get("client_crt")
client_key=MQTT.get("client_key")

global client
ssl.match_hostname = lambda cert, hostname: True
client = mqtt.Client()
if(ssl_enabled == "True"):
    client.tls_set(ca_file, certfile=client_crt,
                                    keyfile=client_key,
                                    tls_version=ssl.PROTOCOL_SSLv23)
    client.connect_async(target, 8883, 60)
else:
    client.connect_async(target, 1883, 60)
    


def IOTG_ZIGBEE_TXPOWER(msg):
#     import ipdb;ipdb.set_trace()
    time.sleep(8)
    power = msg.get('commands')[0].get('power')
    command = msg.get('commands')[0].get('command')
    EUID = msg.get('gateway_euid')
    settings[EUID]['networks'][0]['radio_tx_power'] = power
    publish_settings(settings[EUID])
    return True

def IOTG_ZIGBEE_CH(msg):
#     import ipdb;ipdb.set_trace()
    time.sleep(8)
    channel = msg.get('commands')[0].get('channel')
    command = msg.get('commands')[0].get('command')
    EUID = msg.get('gateway_euid')
    settings[EUID]['networks'][0]['radio_channel'] = channel
    publish_settings(settings[EUID])
    return True

def IOTG_COEX_ENABLE(msg):
#     import ipdb;ipdb.set_trace()
    time.sleep(8)
    coex_enable = msg.get('commands')[0].get('coex_enable')
    command = msg.get('commands')[0].get('command')
    EUID = msg.get('gateway_euid')
    settings[EUID]['networks'][0]['radio_channel'] = coex_enable
    publish_settings(settings[EUID])
    return True

def IOTG_RESTART(msg):
    time.sleep(10)
    EUID = msg.get('gateway_euid')
    publish_settings(settings[EUID])
    return True

def IOTG_VLAN_ENABLE(msg):
#     import ipdb;ipdb.set_trace()
    time.sleep(8)
    iotg_vlan_id = msg.get('commands')[0].get('iotg_vlan_id')
    command = msg.get('commands')[0].get('command')
    EUID = msg.get('gateway_euid')
    if iotg_vlan_id == 0 or iotg_vlan_id == 1:
        settings[EUID]['ap-details'][0]['vlan_id'] = "0"
        settings[EUID]['ap-details'][0]['vlan_enable'] = "0"
    else:
        settings[EUID]['ap-details'][0]['vlan_id'] = str(iotg_vlan_id)
        settings[EUID]['ap-details'][0]['vlan_enable'] = "1"
    publish_settings(settings[EUID])
    return True

def DEVICE_JOIN(msg):
    EUID = msg.get('gateway_euid')
    publish_settings(settings[EUID])
    return True

def IOTG_MODE(msg):
    time.sleep(8)
    mode = msg.get('commands')[0].get('mode')
    command = msg.get('commands')[0].get('command')
    EUID = msg.get('gateway_euid')
    if(mode == 1):
        settings[EUID]['networks'][0]['network_type'] = "ble"
        settings[EUID]['networks'][0]['network_id'] = "NA"
        settings[EUID]['networks'][0]['radio_tx_power'] = "NA"
        settings[EUID]['networks'][0]['radio_channel'] = "NA"
    if(mode == 2):
        settings[EUID]['networks'][0]['network_type'] = "zigbee"
        settings[EUID]['networks'][0]['network_id'] = "0x000"
        settings[EUID]['networks'][0]['radio_tx_power'] = "5"
        settings[EUID]['networks'][0]['radio_channel'] = "12"
    if(mode == 3):
        settings[EUID]['networks'][0]['network_type'] = "zigbee_aa"
        settings[EUID]['networks'][0]['network_id'] = "0x000"
        settings[EUID]['networks'][0]['radio_tx_power'] = "5"
        settings[EUID]['networks'][0]['radio_channel'] = "12"
    publish_settings(settings[EUID])
    return True


def on_message(client, userdata, message):
    if(message.topic  == 'controller/gateway/commands'):
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        command = msg.get('commands')[0].get('command')

        di = {
            'IOTG_ZIGBEE_TXPOWER':IOTG_ZIGBEE_TXPOWER,
            'IOTG_ZIGBEE_CH':IOTG_ZIGBEE_CH,
            'IOTG_COEX_ENABLE':IOTG_COEX_ENABLE,
            'IOTG_VLAN_ENABLE':IOTG_VLAN_ENABLE,
            'IOTG_RESTART':IOTG_RESTART,
            #'DEVICE_JOIN':DEVICE_JOIN,
            'IOTG_MODE':IOTG_MODE
              }
        if command in di:
            if(di[command](msg)):
                print(command," VALUE CONFIGURED")
        else:
            print("COMMAND NOT SUPPORTED")
#         if(command == 'IOTG_ZIGBEE_TXPOWER'):
#             if(IOTG_ZIGBEE_TXPOWER(msg)):
#                 print("TX VALUES APPLIED FOR ",msg.get('gateway_euid'))
#         if(command == 'IOTG_ZIGBEE_CH'):
#             if(IOTG_ZIGBEE_CH(msg)):
#                 print("ZIGBEE VALUES APPLIED FOR ",msg.get('gateway_euid'))
#         if(command == 'IOTG_COEX_ENABLE'):
#             if(IOTG_COEX_ENABLE(msg)):
#                 print("COEX VALUES APPLIED FOR ",msg.get('gateway_euid'))

    else:
        print("OTHER TOPIC RECEIVED")

def Listener():
    client.loop_start()
    client.subscribe("controller/gateway/commands")
    client.on_message=on_message

    time.sleep(1)

def publish_scan_list(Gateway,dongle_mac):
    scan_list_payload =   {
      "gateway_euid": Gateway,
      "devices": [
        {
          "network_mac": dongle_mac,
          "network_id": "0x1234",
          "device_euid": "00:15:8D:00:03:5A:A8:BA",
          "auth": 0,
          "last_seen": 0,
          "lqi": 0,
          "rssi": 0
        },
        {
          "network_mac": dongle_mac,
          "network_id": "0x1234",
          "device_euid": "00:15:8D:00:03:5A:A8:BB",
          "auth": 0,
          "last_seen": 0,
          "lqi": 0,
          "rssi": 0
        }
      ]
    }
    scan_list_payload = json.dumps(scan_list_payload)
    mqtt_res = client.publish(scan_list_topic, scan_list_payload)
    mqtt_res.is_published()

def publish_settings(settings_payload):
    global settings;
    settings[settings_payload.get('gateway_euid')] = settings_payload
    mqtt_res = client.publish(settings_topic, json.dumps(settings_payload))
    return(mqtt_res.is_published())


def publish_heartbeat(Gateway,dongle_mac):
    zigbee_heartbeat_payload = {
  "gateway_euid": Gateway,
  "event_id": 3,
  "event_data": {
    "status": "Online",
    "diagnostics": [
      {
        "network_mac": dongle_mac,
        "network_type": "ble",
        "interface_name": "/dev/ttyUSB100",
        "memory_usage": "4548 bytes",
        "cpu_usage": "0.000000%",
        "network_stack": "EZSP",
        "network_stack_ver": "2.11.3.366",
        "ap_up_time": "9 days, 1:15:20",
        "gateway_up_time": "0 days, 0:00:15",
        "mqtt_qos": "2"
      }
    ]
  }
}
    zigbee_heartbeat_payload = json.dumps(zigbee_heartbeat_payload)
    mqtt_res = client.publish(topic1, zigbee_heartbeat_payload)
    mqtt_res.is_published()




def generate_mac(limit):
    ran = random.randrange(10**80)
    hexstring = "%064x" % ran
    mac = ":".join([hexstring[val:val+2] for val in range(0,len(hexstring), 2)][:limit])
    #print(mac.upper())
    return (mac.upper())
def generate_random_ip():
    ip = []
    for _ in range(4):
        ip.append(str(random.randint(1, 254)))
    return ".".join(ip)

def genetate_tx_power(CC):
    if CC == "US":
        return random.randint(0, 6)
def genetate_channel():
    return random.randint(11, 25)

def generate_name():
    return "Simulated Gateway "+str(random.randint(1111, 9999))

def publish_device_auth(gateway_euid, dongle_mac, device_euid):
    payload = {
  "gateway_euid": gateway_euid,
  "network_mac": dongle_mac,
  "network_id": 0,
  "device_euid": device_euid,
  "device_name": "IKEA of Sweden",
  "device_serial": "11111111",
  "connection_state": 2
}
    device_auth_payload = json.dumps(payload)
    print(device_auth_payload)
    mqtt_res = client.publish(my_topic1, device_auth_payload)
    mqtt_res.is_published()

def publish_device_settings(gateway_euid, dongle_mac, device_euid):
    payload = {
  "gateway_euid": gateway_euid,
  "network_mac": dongle_mac,
  "device_euid": device_euid,
  "device_type": "0x0220",
  "device_manufacturer_name": "IKEA of Sweden",
  "device_model_id": "121",
  "endpoints": [
    {
      "endpoint_id": 1,
      "endpoint_type": "0x0220",
      "in_clusters": [
        "0x0201"
      ],
      "out_clusters": [
        "0x0005",
        "0x0019",
        "0x0020",
        "0x1000"
      ]
    }
  ]
}
    device_settings_payload = json.dumps(payload)
    print(device_settings_payload)
    mqtt_res = client.publish(my_topic2, device_settings_payload)
    mqtt_res.is_published()


def publish_device_function_attibute(gateway_euid, dongle_mac, device_euid):
   payload = {"gateway_euid":gateway_euid,"device_euid":device_euid,"endpoint_id":1,"cluster_id":"0x0201","attributes":[{"attribute_id":"0x0011","status":"0x00","value":"0x02"},{"attribute_id":"0x0012","status":"0x00","value":"0x03"},{"attribute_id":"0x0013","status":"0x00","value":"0x04"},{"attribute_id":"0x0014","status":"0x86","value":"0x05"},{"attribute_id":"0x0015","status":"0x00","value":"0x06"},{"attribute_id":"0x0016","status":"0x00","value":"0x07"},{"attribute_id":"0x0017","status":"0x86","value":"0x08"},{"attribute_id":"0x0018","status":"0x00","value":"0x09"}]}
   i = 0
   while 1:
      device_function_attibute_payload = json.dumps(payload)
      mqtt_res = client.publish(my_topic3, device_function_attibute_payload)
      mqtt_res.is_published()
      time.sleep(15)
      i = i+1
      if i == 4:
         i = 0
         publish_device_settings(gateway_euid, dongle_mac, device_euid)

def initiate_simulation(gateway_euid,dongle_mac):
       device_euid = '24:FD:46:B3:79:E8:8E:07'
       publish_device_auth(gateway_euid, dongle_mac, device_euid)
       publish_device_settings(gateway_euid, dongle_mac, device_euid)
       publish_device_function_attibute(gateway_euid, dongle_mac, device_euid)

import threading
thread = []
threadt = threading.Thread(target=Listener, args=(), kwargs={})
threadt.start()
threadt.join()
for i in range(1):

     thread.append(threading.Thread(target=initiate_simulation, args=("0C:F4:D5:1E:22:10","90:FD:9F:FF:FE:0C:89:CB"), kwargs={}))
for i in range(1):
    thread[i].start()
for i in range(1):
    thread[i].join()
    #print("Added - "+i)

# Listener()
# initiate_simulation(generate_mac(6))
