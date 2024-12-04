import time
import random
import paho.mqtt.client as mqtt
import blynklib

# Configurações do Blynk
BLYNK_AUTH_TOKEN = "qIiGuzOEW-Ec_8PNl08i6cMshL750E9D"
BLYNK_VIRTUAL_PIN = 0

# Configurações do MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "ds/Integer V0"

# Função de callback para o MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao MQTT, código de resposta: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    valor = msg.payload.decode()
    print(f"Mensagem recebida no MQTT: {msg.topic} -> {valor}")
    blynk.virtual_write(BLYNK_VIRTUAL_PIN, valor)
    print(f"Valor enviado para o Blynk (V{BLYNK_VIRTUAL_PIN}): {valor}")

# Configura cliente MQTT
def setup_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

# Configura cliente Blynk
def setup_blynk():
    blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)
    return blynk

# Gera números aleatórios (0 ou 1)
def generate_random_value():
    return random.choice([0, 1])

def main():
    # Inicializa o cliente MQTT
    mqtt_client = setup_mqtt()
    # Inicializa o cliente Blynk
    global blynk
    blynk = setup_blynk()

    # Inicia o loop MQTT
    mqtt_client.loop_start()

    print("Sistema iniciado. Publicando valores...")

    while True:
        # Executa o loop do Blynk
        blynk.run()

        # Gera e publica valores no MQTT
        valor = 1
        mqtt_client.publish(MQTT_TOPIC, valor)
        print(f"Mensagem publicada no MQTT: {valor}")

        # Atraso de 5 segundos
        time.sleep(5)

if __name__ == "__main__":
    main()
