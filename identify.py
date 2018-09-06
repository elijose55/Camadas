from enlace import *
import time
from aplicacao_envia import *

def listen_and_tell(com,tipo_envia,content,tipo_recebe):

	tipo_recebido = 0
	while tipo_recebe != tipo_recebido:

		pack=com.rx.getBufferLen()
		start_time = time.time()

		k=10
		while (pack != k or pack==0) :
			
			temp = time.time() - start_time

			if temp < 5 or pack !=0: 	
				k = pack
				pack=com.rx.getBufferLen()
				time.sleep(1)
				print("Aguardando dados")
				print(pack)

			else:
				start_time = time.time()
				com.sendData(tipo_envia,content)
				print("Mensagem tipo {} não recebida".format(tipo_recebe))
				print(". . . Recontatando . . .")

		head , payload, payloadsize = com.getData(pack)
		#tipo_recebido = int.from_bytes(head[:-2], byteorder='big')
		tipo_recebido = head[7]
		if tipo_recebe != tipo_recebido:
			print("Mensagem de tipo inesperado recebida") 


	return tipo_recebido, head, payload



def only_listen(com,tipo_recebe):
	#melhorar: saber oq fazer com cada byte
	tipo_recebido = 0
	while tipo_recebe != tipo_recebido:

		pack=com.rx.getBufferLen()

		k=10
		while (pack != k or pack==0) :
				
			k = pack
			pack=com.rx.getBufferLen()
			time.sleep(1)
			print("Aguardando dados")
			print(pack)




		head , payload, payloadsize = com.getData(pack)
		#tipo_recebido = int.from_bytes(head[7], byteorder='big')
		tipo_recebido = head[7]
		if tipo_recebe != tipo_recebido:
			print("Mensagem de tipo inesperado recebida") 


	return tipo_recebido, head, payload , payloadsize


def listen_and_tell_double(com,tipo_envia,content,tipo_recebe1,tipo_recebe2):

	tipo_recebido = 0
	while (tipo_recebe1 != tipo_recebido) :

		pack=com.rx.getBufferLen()
		start_time = time.time()

		k=10
		while (pack != k or pack==0) :
			
			temp = time.time() - start_time

			if temp < 5 or pack !=0: 	
				k = pack
				pack=com.rx.getBufferLen()
				time.sleep(1)
				print("Aguardando dados")
				print(pack)

			else:
				start_time = time.time()
				com.sendData(tipo_envia,content)
				print("Mensagem tipo {} ou {} não recebida".format(tipo_recebe1,tipo_recebe2))
				print(". . . Recontatando . . .")

		head , payload, payloadsize = com.getData(pack)
		#tipo_recebido = int.from_bytes(head[7], byteorder='big')
		tipo_recebido = head[7]
		if (tipo_recebe1 != tipo_recebido) and (tipo_recebe2 != tipo_recebido):
			print("Mensagem de tipo inesperado recebida") 
		elif tipo_recebido == tipo_recebe2:
			print("Recebido tipo 6, reenviando pacote ...")


	return tipo_recebido, head, payload