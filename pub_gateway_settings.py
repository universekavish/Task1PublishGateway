# import paho.mqtt.client as mqtt
# import time, ssl, json, random
#
# target = "192.168.247.194"
# topic = "gateway/settings"
import json
import ssl
import paho.mqtt.client as mqtt
import time
import logging
broker = "iot.eclipse.org"
topic = 'gateway/settings'
port = 1883
# payload ={
#       "gateway_euid": "EC:8C:A2:33:BA:E0",
#       "iot_version": "1.5.0.0.1",
#       "networks": [
#         {
#           "network_mac": "00:00:00:00:00:00:00:00",
#           "network_type": "zigbee",
#           "network_id": "",
#           "radio_tx_power": 0,
#           "radio_channel": 0,
#           "iot_coex": 0
#         },
#         {
#           "network_mac": "00:02:5B:A0:86:77",
#           "network_type": "ble",
#           "network_id": "FFFF",
#           "radio_tx_power": "TODO",
#           "radio_channel": "TODO",
#           "iot_coex": 0
#         }
#       ],
#       "ap-details": [
#         {
#           "ip": "192.168.149.48",
#           "mac": "ec:8c:a2:33:ba:e0",
#           "netmask": "255.255.255.0",
#           "gateway": "192.168.149.254",
#           "dns": " 172.19.0.6",
#           "name":"Ruckus AP",
#           "vlan_id": "4",
#           "country_code": "US",
#           "model": "H510",
#           "ap_firmware": "108.1.0.0.15498625",
#           "zone_name": "Default Zone",
#           "apgroup_name": "default",
#           "domain_name": "Administration Domain check",
#           "vlan_enable": "0",
#           "ctl_host": "172.16.112.183",
#           "zone_id": "5db1a5f3-4918-4965-8490-db49401dac16",
#           "domain_id": "dom",
#           "apgroup_id": "b7dd6fa4-50ea-476f-a649-71ea6d1ee155",
#           "usb_power": 0
#         }
#       ]
#     }

payload = {
      "gateway_euid": "EC:8C:A2:33:BA:E0",
      "devices": [
        {
          "network_id": "FFFF",
          "device_euid": "00:00:C0:FB:1E:AA:96:76",
          "auth": 1,
          "last_seen": 0
        },
        {
          "network_id": "FFFF",
          "device_euid": "00:00:CF:EA:1A:2B:6B:08",
          "auth": 1,
          "last_seen": 0
        },
        {
          "network_id": "FFFF",
          "device_euid": "00:00:DC:FB:A1:46:AA:E4",
          "auth": 1,
          "last_seen": 0
        },
        {
          "network_id": "FFFF",
          "device_euid": "00:00:78:A5:04:56:F8:6D",
          "auth": 1,
          "last_seen": 0,
          "network_mac": "90:FD:9F:FF:FE:7C:32:94"
        }
      ]
    }

logging.basicConfig(level=logging.INFO)

def on_log(client, userdata, level, buff):
    logging.info(buff)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        logging.info("Connected")
    else:
        logging.info("Bad connection, returned code = ", str(rc))
        client.loop_stop()
def on_disconnect(client, userdata, fc):
    logging.info("Client disconnected")
def on_publish(client, userdata, mid):
    logging.info("In on_publish callback mid : ", str(mid))

mqtt.Client.connected_flag=False

MQTT = {
  "ca_cert": "/home/asm/Downloads/ruckusCertificates/ca.crt",
  "client_crt": "/home/asm/Downloads/ruckusCertificates/ap.crt",
  "client_key": "/home/asm/Downloads/ruckusCertificates/ap.key"
}

ca_file = MQTT.get("ca_cert")
client_crt = MQTT.get("client_crt")
client_key = MQTT.get("client_key")

client=mqtt.Client()
client.on_log=on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_publish=on_publish

client.tls_set(ca_file, certfile=client_crt, keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)

client.connect(broker, port, 60)
client.loop_start()
while not client.connected_flag:
    print("in wait loop")
    time.sleep(0.3)
time.sleep(3)
print("Publishing")
ret=client.publish(topic, json.dumps(payload))
print("published return = ", ret)
time.sleep(3)
client.loop_stop()
client.disconnect()