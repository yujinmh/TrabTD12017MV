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
		
		fobject = open("denyterms.txt", "r")
		termos = fobject.readlines()
		print(termos)
		termos = ['BLACKLIST_DOMAINS']
		for i in range(0, len(config['BLACKLIST_DOMAINS'])):
    		if config['BLACKLIST_DOMAINS'][i] in url:
        		conn.close()
		return	
		
		return((blacklisturl,whitelisturl))	
	except Exception, ErroArquivos:
		print("Houve um erro no gerenciamento de arquivos de permissoes: ", ErroArquivos)
		sys.exit(1)
	except KeyboardInterrupt:
		print("Interrupcao do usuario.")
		sys.exit(1)

def RespostaProxy(conn, addr, resposta, flags)

def proxy_server(temp, webserver, port, conn, addr, data):  
    ip_host=socket.gethostbyname(webserver)   
    consite=httplib.HTTPSConnection(webserver)
    consite.request("GET","/")
    r1=consite.getresponse()
    print "\n[+] HOST:", webserver
    print "[+] HOST_IP:", ip_host
    print "[+] STATUS: ", r1.status, r1.reason
    consite.close() 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)
        if re.match(".*youtube.*", temp):    
            print "\n[!] YOUTUBE: ", temp
            html='Acesso nao autorizado!'
            conn.send(html)
            conn.close()
            s.send(html)
            s.close()
        while True:
            reply = s.recv(4096)
            if (len(reply)>0):
                conn.send(reply)
                conn_server(reply)
            else:
                break
        s.close()
        conn.close()

    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(2)

	
IniciaSockets()
