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
				tipo_msg = 1
				print("Inicio de transmissao")

				#package_1 = self.tx.criaPackage(data_null, tipo_msg)
				self.sendData(data_null, tipo_msg)
				print("Enviada mensagem do tipo 1")
				self.rx.clearBuffer()

				start_time1 = time.time()
				while True:

					rxBuffer, nRx = self.getData()
					print("head:   " + int.frombytes(rxBuffer[:1], byteorder = "big"))
					if int.frombytes(rxBuffer[:1], byteorder = "big") == 2:
						self.rx.clearBuffer()
						print("Mensagem tipo 2 recebida")
						#package_2 = self.tx.criaPackage(data_null, 3)
						self.sendData(data_null, 3)
						print("Enviada mensagem do tipo 3")
						start_time2 = time.time()
						while True:
							#package_final = self.tx.criaPackage(data, 4)
							self.sendData(data, 4)
							print("Enviada mensagem de tipo 4, aguardando verificação de consitencia")
							time.sleep(0.5)
							rxBuffer, nRx = self.getData()
							if int.frombytes(rxBuffer[:1], byteorder = "big") == 5:

								#package_7 = self.tx.criaPackage(data_null, 7)
								self.sendData(data_null, 7)

								print("Verificacao de consistencia realizada, encerrando comunicacao")
								self.rx.clearBuffer()
								return
							if int.frombytes(rxBuffer[:1], byteorder = "big") == 6:
								self.rx.clearBuffer()
								print("Verificacao de consistencia não conferiu, reenviando pacote")

							if int.frombytes(rxBuffer[:1], byteorder = "big") == 7:
								self.rx.clearBuffer()
								print("Conexao encerrada")
								return

							if keyboard.is_pressed('q'):
								print("Conexao terminada")
								#package_7 = self.tx.criaPackage(data_null, 7)
								self.sendData(data_null, 7)

								return

					if time.time()-start_time1 > 5:
						print("Mensagem tipo 2 não recebida")
						break

			if user == "server":
				data_transmitida = 0
				while True:
					if data_transmitida != 0:
						return data_transmitida
					rxBuffer, nRx = self.getData()
					if int.frombytes(rxBuffer[:1], byteorder = "big") == 1:
						#package_1 = self.tx.criaPackage(data_null, 2)
						self.sendData(data_null, 2)
						print("Recebida mensagem de tipo 1, enviada mensagem do tipo 2 e aguardando mensagem do tipo 3")
						start_time = time.time()
						while True:
							time.sleep(0.5)
							rxBuffer, nRx = self.getData()
							if int.frombytes(rxBuffer[:1], byteorder = "big") == 3:
								self.rx.clearBuffer()
								print("Recebida mensagem de tipo 3, esperando pacote de informações")
								while True:

									time.sleep(1)
									rxBuffer, nRx = self.getData()

									if keyboard.is_pressed('q'):
										print("Conexao terminada")
										#package_7 = self.tx.criaPackage(data_null, 7)
										self.sendData(data_null, 7)

										return

									if int.frombytes(rxBuffer[:1], byteorder = "big") == 7:  #mensagem do tipo 7 (dados)
										print("Conexao encerrando")
										return


									if int.frombytes(rxBuffer[:1], byteorder = "big") == 4:  #mensagem do tipo 4 (dados)

										if int.frombytes(rxBuffer[1:4], byteorder = "big") == nRx:
											data_transmitida = self.getData()
											self.clearBuffer()
											print("Informacoes de payload conferem, enviando mensagem do tipo 5")
											#package_2 = self.rx.criaPackage(data_null, 5)
											self.sendData(data_null, 5)
										else:
											print("Informacoes não confere, enviando mensagem do tipo 6")
											self.sendData(data_null, 6)

							if time.time()-start_time > 5:
								print("Mensagem de tipo 3 não recebida, reenviando mensagem do tipo 2")
								break





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
		print('entrou no getData ')
		data , size = self.rx.getNData()
		payload = self.rx.desfaz_package(data)

		return(payload, len(payload))
