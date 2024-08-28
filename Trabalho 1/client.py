# importa a biblioteca para a conexão
from socket import *

# configura o cliente
server_name = 'localhost'
server_port = 12000

# cria o socket UDP
SocketCliente = socket(AF_INET, SOCK_DGRAM)

# menu de atendimento
menu = "Chatbot do provedor de internet SRS-net.\nTecle 1 para agendar uma visita técnica\nTecle 2 para saber mais sobre sua fatura"
menu += "\nTecle 3 para conhecer nossas promoções\nTecle 4 para encerrar o atendimento"
print(f"\n{menu}")

# chatbot
while True:
    # solicita a escolha do usuário
    mensagem = input("\nVocê: ")
    
    # envia para o servidor
    SocketCliente.sendto(mensagem.encode('utf-8'), (server_name, server_port))

    # recebe a resposta do servidor
    resposta, _ = SocketCliente.recvfrom(1024)
    print("Chatbot:", resposta.decode('utf-8'))

    # encerra a conexão se o cliente solicitar
    if "Encerrando atendimento, tenha um bom dia!" in resposta.decode('utf-8'):
        break