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

# Threads
import threading

# Class
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen = self.fisica.write(self.buffer)
                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)


    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)


    def criaPackage(self, payload, package_number, total_packages, package_error, message_type, crc):
        #(numero do pacote, total de pacotes, erro/pacote esperado, size do payload(3), CRC(3), tipo da msg)

        #pega os dados e empacota com HEAD, EOP e byte Stuffing

        byte_stuff = bytes.fromhex("FF AA FE FD FC")
        eop = bytes.fromhex("FF FE FD FC")
        payload_size = len(payload)
        print('--------------------')
        print('tamanho do payload:',payload_size)


        #cria o HEAD
        payload_head = (payload_size).to_bytes(3, byteorder = "big")        #tamanho do payload
        message_type = (message_type).to_bytes(1, byteorder = "big")        #tipo de mensagem
        package_number = (package_number).to_bytes(1, byteorder = "big")    #numero do pacote
        total_packages = (total_packages).to_bytes(1, byteorder = "big")    #total de pacotes
        package_error = (package_error).to_bytes(1, byteorder = "big")      #erro de pacote 
        crc_payload = (crc).to_bytes(3, byteorder = "big")                  #crc do payload

        und = bytes(5)


        head = package_number + total_packages + package_error + payload_head + crc_payload + message_type

        check = payload.find(eop)
        if check != -1:
            payload = payload.replace(eop, byte_stuff)


        package = head + payload + eop
        overhead = len(package) / len(payload)
        print("overHead:{0}".format(overhead))
        print('--------------------')
        return package, len(payload)

