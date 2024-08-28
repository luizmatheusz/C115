# importa a biblioteca para a conexão
from socket import *

# configura o servidor
PortaServidor = 12000

# cria o socket UDP
SocketServidor = socket(AF_INET, SOCK_DGRAM)
SocketServidor.bind(('', PortaServidor))
SocketServidor.settimeout(1000)

# menu de atendimento
menu = "Chatbot do provedor de internet SRS-net.\nTecle 1 para agendar uma visita técnicaTecle 2 para saber mais sobre sua fatura"
menu += "Tecle 3 para conhecer nossas promoções\nTecle 4 para encerrar o atendimento"

# print de inicialização do servidor
print("Servidor iniciado.")

# recepção das mensagens
while 1:
	# recebe a primeira mensagem do cliente
	mensagem, endereco_cliente = SocketServidor.recvfrom(1024)
	mensagem = mensagem.decode('utf-8')

	# analisa a mensagem recebida
	if mensagem == "1":
		resposta = "Visita técnica agendada!"
	elif mensagem == "2":
		resposta = "Fatura atual: 30/08/2024. Valor: R$ 79,90."
	elif mensagem == "3":
		resposta = "Conheça o plano Premium, com 500GB de internet por apenas R$ 139,90!!"
	elif mensagem == "4":
		resposta = "Encerrando atendimento, tenha um bom dia!"
		SocketServidor.sendto(resposta.encode('utf-8'), endereco_cliente)
		print("\nConexão encerrada pelo cliente.")
		break
	else:
		resposta = "Opção inválida. Tente novamente."

	# envia a resposta para o cliente
	SocketServidor.sendto(resposta.encode('utf-8'), endereco_cliente)
 
	# retorno das informações para o próprio servidor
	print(f"\nCliente: {mensagem}")
	print(f"Servidor: {resposta}")