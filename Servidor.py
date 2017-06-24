from socket import *
from thread import *
import sys

def IniciaSockets():	#Funcao que inicia sockets e comeca a ouvir requisicoes do browser
	try:
		server = socket(AF_INET, SOCK_STREAM)
		server.bind(('', 5509))
		server.listen(5)
		print("Ouvindo...")
	except Exception, ErroSocket:
		print("Socket nao foi iniciado: ", ErroSocket)
		sys.exit(2)

	while 1:
		try:
			conn, addr = server.accept()
			print("Conexao aceita.")
			resposta = conn.recv(1024)
			print("Houve resposta!: ", resposta)
			start_new_thread(Tratamento, (conn, addr, resposta))
		except Exception, ErroConn:
			print("Nao houve resposta ou a conexao nao foi aceita: ", ErroConn)
			sys.exit(1)
		except KeyboardInterrupt:
			server.close()
			print("\nInterrupcao do usuario.")
			sys.exit(1)

def Tratamento(conn, addr, resposta):
	try:
		aux = resposta.split('\r')[0]
		link = aux.split(' ')
		url = link[1]
		print(url)
		flags = VerificaArquivos(resposta, url)
		RespostaProxy(conn, addr, resposta, flags)
	except Exception, ErroString:
		print("Erro no tratamento da resposta: ", ErroString)
		sys.exit(2)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

def VerificaArquivos(resposta, url):
	try:
		fobject = open("blacklist.txt", "r")  #blacklist: tratamento
		proibidos = fobject.readlines()
		if url in proibidos:
			blacklisturl = 1
		else:
			blacklisturl = 0
		fobject.close()

		fobject = open("whitelist.txt", "r")
		permitidos = fobject.readlines()
		print(permitidos)
		if url in permitidos:
			whitelisturl = 1
		else:
			whitelisturl = 0
		fobject.close()

		return((blacklisturl,whitelisturl))	
	except Exception, ErroArquivos:
		print("Houve um erro no gerenciamento de arquivos de permissoes: ", ErroArquivos)
		sys.exit(1)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

def RespostaProxy(conn, addr, resposta, flags)
	
	
IniciaSockets()
