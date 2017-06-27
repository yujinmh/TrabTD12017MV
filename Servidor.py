from socket import *
from thread import *
from time import *
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
	except KeyboardInterrupt:
		printf("Interrupcao do usuario.")
		sys.exit(1)
			
	while 1:
		try:
			resposta = ""
			conn, addr = server.accept()
			print("Conexao aceita.")
			resposta = conn.recv(1024)
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
		host = ""
		aux = ""
		aux = resposta.split('\r')[0]
		link = aux.split(' ')
		aux2 = link[1]
		i = aux2.find("://") # requisicoes http:// ou https://
		if (i == -1):
			aux3 = aux2
		else:
			aux3 = aux2[(i+3):]
		j = aux3.find(":")
		if j==-1:
			aux4 = aux3
		else:
			aux4 = aux3[:j]
		k = aux4.find("/")
		if k == -1:
			host=aux4
		else:
			host = aux4[:k]
		print(host)
		flags = VerificaArquivos(conn, resposta, host)
		RespostaProxy(conn, addr, resposta, flags, host)
	except Exception, ErroString:
		print("Erro no tratamento da resposta: ", ErroString)
		sys.exit(2)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

def VerificaArquivos(conn, resposta, host):
	try:
		fobject = open("blacklist.txt", "r")  
		proibidos = fobject.read().splitlines()
		if host in proibidos:
			blacklisturl = 1
		else:
			blacklisturl = 0
		fobject.close()

		fobject = open("whitelist.txt", "r")
		permitidos = fobject.read().splitlines()
		if host in permitidos:
			whitelisturl = 1
		else:
			whitelisturl = 0
		fobject.close()

		fobject = open("denyterms.txt", "r")
		termos = fobject.read().splitlines()
		for termo in termos:
			sleep(1)
			if termo in resposta:
				temdeny = 1
			else:
				temdeny = 0
		if (whitelisturl==1 and temdeny == 1):
			whitelisturl=0
		if (blacklisturl==0 and temdeny == 1):
			blacklisturl == 1

		return((blacklisturl,whitelisturl))	
	except Exception, ErroArquivos:
		print("Houve um erro no gerenciamento de arquivos de permissoes: ", ErroArquivos)
		sys.exit(1)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

def RespostaProxy(conn, addr, resposta, flags, host):
	blacklisturl = flags[0]
	whitelisturl = flags[1]
	try:
		if (blacklisturl==0 and whitelisturl==1):
			proxysocket = socket(AF_INET, SOCK_STREAM)
			print(host)
			print(resposta)
			proxysocket.connect((host, 80))
			proxysocket.send(resposta)
			while True:
				recebeu = proxysocket.recv(8192)
				if len(recebeu)>0:
					fobj = open("Memoria.txt", "a")
					tamanho = len(recebeu)
					fobj.writelines(recebeu)
					conn.send(recebeu)
				else:
					break
			fobj.close()
			proxysocket.close()
			conn.close()
			sys.exit(1)
		elif(blacklisturl==1):
			print("Site Bloqueado: Esta na Blacklist ou tem deny terms.")
			sys.exit()
		elif(whitelisturl==0):
			print("Site nao esta na whitelist ou tem deny terms.")
			sys.exit(1)

	except Exception, ErroRespostaProxy:
		print("Houve um erro ao postar a resposta: ", ErroRespostaProxy)
		sys.exit(1)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

	
IniciaSockets()
