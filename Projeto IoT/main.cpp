#define BLYNK_TEMPLATE_ID "ID"
#define BLYNK_TEMPLATE_NAME "NAME"

#include <WiFi.h>
#include <PubSubClient.h>
#include <BlynkSimpleEsp32.h>

// Wi-Fi
const char* ssid = "REDE";
const char* password = "SENHA";

// Auth Token do Blynk
char auth[] = "TOKEN";  // Substitua pelo seu Auth Token do Blynk

// Configuração do broker MQTT
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

const int magneticSwitchPin = 5; // Pino de conexão

// Funções para MQTT
void mqttCallback(char* topic, byte* payload, unsigned int length);
void reconnectMQTT();

void setup() {
  Serial.begin(115200);

  // Conectar ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao Wi-Fi...");
  }
  Serial.println("Wi-Fi conectado!");

  // Configurar MQTT
  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(mqttCallback);

  // Conectar ao Blynk
  Blynk.begin(auth, ssid, password);
}

void loop() {
  // Executar tarefas do Blynk
  Blynk.run();

  // Reconectar ao MQTT se necessário
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  // Verificar o estado do sensor magnético
  int sensorState = digitalRead(magneticSwitchPin);
  String mensagem;

  if (sensorState == LOW) { // LOW = Porta aberta (quando o ímã está longe)
    mensagem = "Porta Aberta";
  } else { // HIGH = Porta fechada (quando o ímã está próximo)
    mensagem = "Porta Fechada";
  }

  // Enviar mensagem para o MQTT
  mqttClient.publish("ds/statusPorta", mensagem.c_str());
  mqttClient.publish("ds/valorSensor", mensagem.c_str());
  Serial.println("Mensagem enviada: " + mensagem);

  delay(5000); // Enviar mensagem a cada 5 segundos
}

// Reconectar ao MQTT
void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado ao MQTT!");
      mqttClient.subscribe("ds/valorSensor");
      mqttClient.subscribe("ds/statusPorta");
    } else {
      Serial.println("Falha ao conectar. Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

// Callback para mensagens MQTT
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida no tópico: ");
  Serial.println(topic);

  String mensagem = "";
  for (unsigned int i = 0; i < length; i++) {
    mensagem += (char)payload[i];
  }
  Serial.println("Mensagem: " + mensagem);

  // Atualizar status no Blynk
  if (String(topic) == "ds/statusPorta") {
    Blynk.virtualWrite(V1, mensagem.c_str());
  }

  else if (String(topic) == "ds/valorSensor") {
    Blynk.virtualWrite(V0, mensagem.c_str());
  }
}