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

import keyboard

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
		print("teste")
		while True:

			if user == "client":
				print("Inicio de transmissao")
				self.sendData(data_null, 1)
				print("Enviada mensagem do tipo 1")
				self.rx.clearBuffer()
				start_time1 = time.time()

				while True:
					start_time2 = time.time()
					rxBuffer, nRx = self.getData()
					while rxBuffer == 0 and (start_time2-start_time1)<5:
						print("Esperando tipo 2")
						rxBuffer, nRx = self.getData()
						start_time2 = time.time()

					if rxBuffer == 0:
						print("Mensagem tipo 2 não recebida")
						break

					else:
						tipo_msg = self.getType(rxBuffer)
						print("tipo.:   " + tipo_msg)

						if tipo_msg == 2:
							self.rx.clearBuffer()
							print("Mensagem tipo 2 recebida")

							self.sendData(data_null, 3)
							self.rx.clearBuffer()
							print("Enviada mensagem do tipo 3")
							start_time2 = time.time()

							while True:
								self.sendData(data, 4)
								self.rx.clearBuffer()
								start_time1 = time.time()
								print("Enviada mensagem de tipo 4, aguardando verificação de consitencia")
								time.sleep(0.5)
								rxBuffer, nRx = self.getData()
								start_time2 = time.time()

								while rxBuffer == 0 and (start_time2-start_time1)<5:
									rxBuffer, nRx = self.getData()
									start_time2 = time.time()

								if rxBuffer != 0:

									tipo_msg = self.getType(rxBuffer)
									print("head..:   " + tipo_msg)

									if tipo_msg == 5:
										#package_7 = self.tx.criaPackage(data_null, 7)
										self.sendData(data_null, 7)
										print("Verificacao de consistencia realizada, encerrando comunicacao")
										self.rx.clearBuffer()
										return

									if tipo_msg == 6:
										self.rx.clearBuffer()
										print("Verificacao de consistencia não conferiu, reenviando pacote")

									if tipo_msg == 7:
										self.rx.clearBuffer()
										print("Conexao encerrada")
										return
								else:
									print("Resposta não recebida")


								if keyboard.is_pressed('q'):
									print("Conexao terminada")
									self.sendData(data_null, 7)

									return
						else:
							print("mensagem recebida nao eh tipo 2")
							break


			if user == "server":
				data_transmitida = 0
				while True:

					if data_transmitida != 0:
						return data_transmitida

					rxBuffer, nRx = self.getData()
					while rxBuffer == 0:
						print("Recebendo")
						rxBuffer, nRx = self.getData()

					tipo_msg = self.getType(rxBuffer)
					print("head..:   " + tipo_msg)

					if tipo_msg == 1:
						print("mensagem tipo 1 recebida")

						while True:
							self.sendData(data_null, 2)
							start_time1 = time.time()
							print("enviada mensagem do tipo 2 e aguardando mensagem do tipo 3")
							self.rx.clearBuffer()
							time.sleep(0.5)

							rxBuffer, nRx = self.getData()
							start_time2 = time.time()
							while rxBuffer == 0 and (start_time2-start_time1)<5:
								print("aguardando tipo 3")
								start_time2 = time.time()
								rxBuffer, nRx = self.getData()
							if rxBuffer == 0:
								print("mensagem tipo 3 nao recebida")
							else:
								tipo_msg = self.getType(rxBuffer)
								print("head..:   " + tipo_msg)

								if tipo_msg == 3:
									self.rx.clearBuffer()
									print("Recebida mensagem de tipo 3, esperando pacote de informações")
									while True:
										time.sleep(1)
										rxBuffer, nRx = self.getData()
										while rxBuffer == 0:
											print("recebendo")
											rxBuffer, nRx = self.getData()

										tipo_msg = self.getType(rxBuffer)

										if keyboard.is_pressed('q'):
											print("Conexao terminada")
											#package_7 = self.tx.criaPackage(data_null, 7)
											self.sendData(data_null, 7)
											return

										if tipo_msg == 7:  #mensagem do tipo 7 (dados)
											print("Conexao encerrando")
											return data_null

										if tipo_msg == 4:  #mensagem do tipo 4 (dados)
											payload = self.rx.desfaz_package(rxBuffer)

											if payload == 1:
												print("Informacoes não confere, enviando mensagem do tipo 6")
												self.sendData(data_null, 6)

											else:
												self.clearBuffer()
												print("Informacoes de payload conferem, enviando mensagem do tipo 5")
												self.sendData(data_null, 5)
												return payload
								else:
									print("tipo de mensagem errado recebido")





	def sendData(self, data, tipo_msg):
		""" Send data over the enlace interface
		"""

		pacote, lenPayload = self.tx.criaPackage(data,tipo_msg)
		self.tx.sendBuffer(pacote)
		return lenPayload


	def getData(self):
		""" Get n data over the enlace interface
		Return the byte array and the size of the buffer
		"""
		data, size = self.rx.getNData()
		#payload = self.rx.desfaz_package(data)

		return(data, size)

	def getType(self, package):
		print(package)
		print(package[:2])
		print("teste")
		tipo = int.frombytes(package[:2], byteorder = "big")
		return tipo

