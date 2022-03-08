# import paho.mqtt.client as mqtt
# import time
# import ssl

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
#
# broker="192.168.247.194"
# port=8883
#
# def on_publish(client, userdata, result):
#     print("Topic published")
#     pass
#
#
# client1=mqtt.Client("control")
#
# #client1.tls_set('/home/asm/Downloads/ruckusCertificates/ca.crt', tls_version=2)
# #client1.tls_set('/home/asm/Downloads/ruckusCertificates/ap.key', tls_version=2)
# #client1.tls_set('/home/asm/Downloads/ruckusCertificates/ap.crt', tls_version=2)
#
# client1.tls_set("/home/asm/Downloads/ruckusCertificates/ca.crt",
# certfile="/home/asm/Downloads/ruckusCertificates/ap.crt",
# keyfile="/home/asm/Downloads/ruckusCertificates/ap.key",
# tls_version=ssl.PROTOCOL_SSLv23
#                )
#
# client1.on_publish = on_publish
# client1.connect(broker, port)
# ret=client1.publish("gateway/settings", "On")


# import json
#
# import paho.mqtt.client as mqtt
# import ssl
#
# target = '192.168.247.194'
# topic = 'gateway/settings'
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
# ssl_enabled = True
# ssl.match_hostname = lambda cert, hostname: True
# MQTT = {
#   "ca_cert": "/home/asm/Downloads/ruckusCertificates/ca.crt",
#   "client_crt": "/home/asm/Downloads/ruckusCertificates/ap.crt",
#   "client_key": "/home/asm/Downloads/ruckusCertificates/ap.key"
# }
#
# ca_file = MQTT.get("ca_cert")
# print("Working 1")
# client_crt = MQTT.get("client_crt")
# client_key = MQTT.get("client_key")
# print("Working 2")
# client1 = mqtt.Client()
# print("Working 3")
# # client1.tls_set_context(context=None)
# if ssl_enabled:
#   client1.tls_set(ca_file, certfile=client_crt, keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)
#   print("Working 4")
#   client1.connect_async('192.168.247.194', 8883, 60)
#   print("Working 5")
# else:
#   client1.connect_async('192.168.247.194', 8883, 60)
#   print("Working 6")
#
# client1.publish(topic, json.dumps(payload))
# print("Working 7")


import paho.mqtt.client as mqtt
import time,sys,ssl,json

target = '192.168.247.194'
topic = 'gateway/settings'

# def on_connect(client, rc):
#     client.connect(target)
#     client.publish(topic, json.dumps(payload))


ssl.match_hostname = lambda cert, hostname: True
MQTT = {
    "ca_cert": "/home/asm/Downloads/ruckusCertificates/ca.crt",
    "client_crt": "/home/asm/Downloads/ruckusCertificates/ap.crt",
    "client_key": "/home/asm/Downloads/ruckusCertificates/ap.key"
}

ca_file=MQTT.get("ca_cert")
client_crt=MQTT.get("client_crt")
client_key=MQTT.get("client_key")

ssl_enabled = True

client = mqtt.Client(mqtt.MQTTv31)
client2 = mqtt.Client(mqtt.MQTTv)
#client.on_connect = on_connect
client.subscribe(topic)
if(ssl_enabled == True):
    client.tls_set(ca_file, certfile=client_crt,
                                    keyfile=client_key,
                                    tls_version=ssl.PROTOCOL_SSLv23)
    print("1")
    client.connect_async(target, 8883, 60)
    print("2")
    client.publish(topic, json.dumps(payload))
    print("3")
else:
    client.connect(target, 8883, 60)


#client.publish(topic, json.dumps(payload))

