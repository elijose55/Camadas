#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

import crc16


# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
	""" This class implements methods to the interface between Enlace and Application
	"""

	def __init__(self, name):
		""" Initializes the enlace class
		"""
		self.fisica      = fisica(name)
		self.rx          = RX(self.fisica)
		self.tx          = TX(self.fisica)
		self.connected   = False

	def enable(self):
		""" Enable reception and transmission
		"""
		self.fisica.open()
		self.rx.threadStart()
		self.tx.threadStart()

	def disable(self):
		""" Disable reception and transmission
		"""
		self.rx.threadKill()
		self.tx.threadKill()
		time.sleep(1)
		self.fisica.close()

	################################
	# Application  interface       #
	################################

	def comunicacao(self, data, user):
		data_null = (0).to_bytes(4, byteorder = "big")
		while True:

			if user == "client":

				print("Enviada mensagem do tipo 1")
				self.sendData(data_null, 0, 0, 0, 1, 0)
				
				start_time1 = time.time()

				size = self.waitLoop(2,1)

				if size != 0:
					print('...')
					rxBuffer = self.getData(size)
					tipo_msg = self.getType(rxBuffer)

					if tipo_msg == 2:
						print("Mensagem tipo 2 recebida")
						print('----------------------')
						time.sleep(2.5)
						print("Enviada mensagem do tipo 3")
						self.sendData(data_null, 0, 0, 0, 3, 0)
						time.sleep(1)

						self.sendPackages(data)
						print("Transmissao Concluida")
						print("Enviando Mensagem de tipo 7 (encerramento)")
						time.sleep(5)
						self.sendData(data_null, 0, 0, 0, 7, 0)
						break
					elif tipo_msg == 7:
						print("Mensagem de encerramento recebida - encerrando")
						break
					else:
						print('--------------------')
						print("Erro de mensagem recebida1")
						print('--------------------')

				else:
					print('--------------------')
					print("Mensagem tipo 2 não recebida")
					print('--------------------')


			if user == "server":
				while True:

					size = self.waitLoop(2,0)

					rxBuffer = self.getData(size)
					tipo_msg = self.getType(rxBuffer)
					print('tipo',tipo_msg)

					if tipo_msg == 1:
						print('--------------------')
						print("Mensagem de tipo 1 recebida")

						while True:
							print("Enviada mensagem do tipo 2")
							self.sendData(data_null, 0, 0, 0, 2, 0)
							self.rx.clearBuffer()

							size = self.waitLoop(3,1)
							#rxBuffer = self.getData(size)

							if size == 0:
								print('--------------------')
								print("Mensagem de tipo 3 não recebida")
								print('--------------------')
							else:
								rxBuffer = self.getData(size)
								tipo_msg = self.getType(rxBuffer)

								if tipo_msg == 3:
									print('--------------------')
									print("Recebida mensagem de tipo 3, esperando pacote de informações")
									print('--------------------')
									while True:
										time.sleep(0.3)
										size = self.waitLoop(4,0)

										rxBuffer = self.getData(size)
										tipo_msg = self.getType(rxBuffer)


										if tipo_msg == 7:  #mensagem do tipo 7 (dados)
											print("Mensagem de encerramento recebida - encerrando")
											return data_null

										elif tipo_msg == 4:  #mensagem do tipo 4 (dados)

											full_data = self.receivePackages()
											print('Em Espera')
											size = self.waitLoop(9,0)

											rxBuffer = self.getData(size)
											tipo_msg = self.getType(rxBuffer)

											if tipo_msg == 7:  #mensagem do tipo 7 (dados)
												print('--------------------')
												print("Mensagem de tipo 7 recebida")
												print('--------------------')
												print("Conexao encerrando")
												return full_data
										else:
											print('--------------------')
											print("Erro de Mensagem recebida4")
											print('--------------------')
								elif tipo_msg == 7:
									print("Mensagem de encerramento recebida - encerrando")
									return data_null

								else:
									print('--------------------')
									print("Erro de Mensagem recebida2")
									print('--------------------')
					elif tipo_msg == 7:
						print("Mensagem de encerramento recebida - encerrando")
						return data_null
					else:
						print("Erro de mensagem recebida3")




	def sendData(self, data, numero_pacote, pacotes_totais, erro_pacote, tipo_msg, crc):
		""" Send data over the enlace interface
		(self, payload, package_number, total_packages, package_error, message_type)
		"""
		pacote, lenPayload = self.tx.criaPackage(data, numero_pacote, pacotes_totais, erro_pacote, tipo_msg, crc)
		self.tx.sendBuffer(pacote)
		return lenPayload

	def sendPackages(self, data):
		print("...Inicio da transmissao dos pacotes de dados...")
		total_packages = int((len(data)/128)+1)
		lista_packages = []
		i = 0
		idx = 0
		info = data

		while len(info)>128:
			pay = info[:128]
			info = info[128:]
			lista_packages.append(pay)
		lista_packages.append(info)

		#while i<(len(data)-128):
		#	lista_packages.append(data[i:i+127])
		#	i+=128
		#lista_packages.append(data[i:])
		print('Pacotes totais:',total_packages)
		print("{0} pacotes a serem enviados".format(len(lista_packages)))

		while idx < len(lista_packages):
			time.sleep(1)
			val = lista_packages[idx]
			while True:
				print("------------------------------")
				print("Pacote {0} enviado".format(idx))
				print("Tamanho:",len(val))
				print(self.crc16(val))
				self.sendData(val, idx, total_packages, 0, 4, self.crc16(val)+1)
				size = self.waitLoop(5,1)
				if size !=0 :
					break
				else:
					print("Resposta nao recebida")
			rxBuffer = self.getData(size)
			tipo_msg = self.getType(rxBuffer)

			if tipo_msg == 5:
				print("Mensagem tipo 5 recebida")
				idx+=1
			elif tipo_msg == 6:
				print("Mensagem tipo 6 recebida")	
			elif tipo_msg == 8:
				print("Mensagem tipo 8 recebida")
				if self.getExpectedPackage(rxBuffer) == -1:
					print("Erro de Mensagem")
				else:
					idx = self.getExpectedPackage(rxBuffer)
			elif tipo_msg == 7:
				print("Mensagem de encerramento recebida - encerrando tudo")
				return
			else:
				print("Erro de Mensagem")
		print("Transmissao dos pacotes concluida")
		return		



	def receivePackages(self):
		print("...Inicio da recepcao dos pacotes de dados...")
		pacote_esperado = 0
		lista_packages = bytes(0)
		data_null = (0).to_bytes(4, byteorder = "big")

		while True:
			size = self.waitLoop(9,0)
			rxBuffer = self.getData(size)
			if rxBuffer == 51:
				print("Erro de mensagem")
				self.sendData(data_null, 0, 0, 0, 6, 0)
			else:

				pacotes_totais = rxBuffer[1]
				tipo_msg = self.getType(rxBuffer)

				if tipo_msg == 4:
					
					if self.getPackageNumber(rxBuffer) == pacote_esperado:
						if self.crcIsCorrect(rxBuffer):
							print('_____________________')
							print("Pacote recebido: {0}".format(self.getPackageNumber(rxBuffer)))
							print("Pacote esperado: {0}".format(pacote_esperado))
							print("Correto! - Mensagem de tipo 5 enviada")
							self.sendData(data_null, 0, 0, 0, 5, 0)
							package = self.getPackage(rxBuffer)
							print(self.crc16(package))
							lista_packages += package
							pacote_esperado += 1
							print('Pacotes a serem recebidos:',(pacotes_totais-pacote_esperado))
							if pacotes_totais-pacote_esperado == 0:
								print("Todos os {0} pacotes recebidos".format(pacote_esperado))
								full_data = lista_packages
								print("Os dados recebidos tem {0} bytes".format(len(full_data)))
								break
						else:
							print("Pacote corrompido - CRC incorreto")
							time.sleep(1)
							print("Enviada mensagem de tipo 6")
							self.sendData(data_null, 0, 0, 0, 6, 0)

					else:
						print('_____________________')
						print("Pacote recebido: {0}".format(self.getPackageNumber(rxBuffer)))
						print("Pacote esperado: {0}".format(pacote_esperado))
						print("Incorreto! - Mensagem de tipo 8 enviada")
						time.sleep(1)
						self.sendData(data_null, 0, 0, pacote_esperado, 8, 0)

				elif tipo_msg == 7:
					print('Mensagem de tipo 7 recebida - comunicacao encerrando')
					break
		print('Transmissao dos pacotes encerrada')
		return full_data





	def getData(self,size):
		""" Get n data over the enlace interface
		Return the byte array and the size of the buffer
		"""
		buffer_data = self.rx.getNData(size)
		data = self.rx.desfaz_package(buffer_data)


		return(data)

	def getType(self, data):
		#null, tipo_msg = self.rx.desfaz_package(package)
		if data == 51:
			return data
		tipo_msg = data[9]
		return tipo_msg

	def getPackage(self, data):
		if data == 51:
			return data
		package = data[10:]
		return package

	def getPackageNumber(self, data):
		if data == -1:
			return data
		package_number = data[0]
		return package_number

	def getExpectedPackage(self, data):
		if data == -1:
			return data
		expected_type = data[2]
		return expected_type
	def crcIsCorrect(self,data):
		expected_crc = int.from_bytes(data[6:9], byteorder = "big")
		true_crc = self.crc16(self.getPackage(data))
		if expected_crc == true_crc:
			return True
		else:
			return False

	def waitLoop(self,type,timed):
		size = 10
		start_time1 = time.time()
		if timed == 1:
			while (self.rx.getBufferLen() == 0 or self.rx.getBufferLen() > size) and (time.time()-start_time1)<5:
				if(type==9):
					print('.')
				else:
					print("Esperando tipo {0}".format(type))
				time.sleep(0.5)
				size = self.rx.getBufferLen()
		if timed == 0:
			while self.rx.getBufferLen() == 0 or self.rx.getBufferLen() > size:
				print("Recebendo")
				time.sleep(0.3)
				size = self.rx.getBufferLen()
		return size


	def crc16(self, data: bytes):

		return crc16.crc16xmodem(data)
