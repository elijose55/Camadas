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
        data_null = b"0x00"
        while True:
            if user == "client":
                tipo_msg = 1

                package_1 = self.tx.criaPackage(data_null, tipo_msg)
                self.sendData(package)
                print("Enviada mensagem do tipo 1")

                start_time1 = time.time()
                while True:
                    rxBuffer, nRx = self.getData()
                    if int.frombytes(rxBuffer[:1], byteorder = "big") == 2:
                        self.rx.clearBuffer()
                        print("Mensagem tipo 2 recebida")
                        package_2 = self.tx.criaPackage(data_null, 3)
                        self.sendData(package_2)
                        print("Enviada mensagem do tipo 3")
                        start_time2 = time.time()
                        while True:
                            package_final = self.tx.criaPackage(data, 4)
                            self.sendData(package_final)
                            print("Enviada mensagem de tipo 4, aguardando verificação de consitencia")
                            time.sleep(0.5)
                            rxBuffer, nRx = self.getData()
                            if int.frombytes(rxBuffer[:1], byteorder = "big") == 5:
                                print("Verificacao de consistencia realizada, encerrando comunicacao")

                                self.rx.clearBuffer()
                                return
                            if int.frombytes(rxBuffer[:1], byteorder = "big") == 6:
                                self.rx.clearBuffer()
                                print("Verificacao de consistencia não conferiu, reenviando pacote")

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
                        package_1 = self.tx.criaPackage(data_null, 2)
                        self.sendData(package_1)
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
                                    if int.frombytes(rxBuffer[1:4], byteorder = "big") == nRx:
                                        data_transmitida = self.getData()
                                        self.clearBuffer()
                                        print("Informacoes de payload conferem, enviando mensagem do tipo 5")
                                        package_2 = self.rx.criaPackage(data_null, 5)
                                        self.sendData(package_2)
                                        break
                                    else:
                                        print("Informacoes não confere, enviando mensagem do tipo 6")
                                        package_3 = self.sendData(data_null, 6)

                            if time.time()-start_time > 5:
                                print("Mensagem de tipo 3 não recebida, reenviando mensagem do tipo 2")
                                break





    def sendData(self, data):
        """ Send data over the enlace interface
        """

        pacote, lenPayload = self.tx.criaPackage(data)
        self.tx.sendBuffer(pacote)
        return lenPayload


    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ')
        data , size= self.rx.getNData()
        payload = self.rx.desfaz_package(data)

        return(payload, len(payload))
