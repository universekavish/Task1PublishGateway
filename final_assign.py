import json
import paho.mqtt.client as mqtt
import time
import ssl

# def ssl_prep():
#     ssl_context = ssl.create_default_context()
#     ssl_context.load_cert_chain(certfile="/home/asm/Downloads/ca.crt")
#     ssl_context.load_cert_chain(certfile="/home/asm/Downloads/ap.crt", keyfile="/home/asm/Downloads/ap.key")
#     return ssl_context

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

target = "10.157.96.124"
#target = "10.157.96.28"
topic = "gateway/settings"
port = 8883

ssl_enabled = True

MQTT = {
    "ca_cert": "/cafiles/ca.crt",
    "client_crt": "/cafiles/mqttclient.crt",
    "client_key": "/cafiles/mqttclient.key"
}

ca_cert = MQTT.get("ca_cert")
client_crt = MQTT.get("client_crt")
client_key = MQTT.get("client_key")
global client1
client1 = mqtt.Client()
if(ssl_enabled == True):
    ssl.match_hostname = lambda cert, hostname: True
    client1.tls_set(ca_cert, certfile=client_crt, keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)
    client1.connect(target, port, 60)
#    ssl_context = ssl_prep()
#    client1.tls_set_context(context=ssl_context)
    result = client1.publish(topic, json.dumps(payload))
    result.is_published()
else:
    client1.connect(target, 1883, 60)
