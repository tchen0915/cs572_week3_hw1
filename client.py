#!/usr/bin/env python

import binascii

from socket import *
from random import seed
from random import randint

from ctr import decrypt, encrypt, KEY, key_bytes
from config import HOST, PORT, BUFSIZ, ADDR

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

print("Client attempting connection to : {} port: {}".format(HOST, PORT))
print("Connection established...")

seed(99)
randomValue = randint(1000000, 9999999)
print("A Client send a random number {} to the server.".format(randomValue))
tcpCliSock.send(str(randomValue).encode('utf-8'))

iv = tcpCliSock.recv(BUFSIZ)
tcpCliSock.send("received".encode('utf-8'))
ciphertext = tcpCliSock.recv(BUFSIZ)
print("Read a cipher text : {}".format(str(binascii.hexlify(ciphertext), 'ascii')))
plaintext = decrypt(KEY, iv, ciphertext)
print("Decrypted plaintext: " + str(plaintext, 'ascii'))

input("Press Enter to continue")

while True:
  data = input('> ')
  # For example, if the server side
  # type Return without entering any
  # message to end communication.
  if not data:
    break
  tcpCliSock.send(data.encode('utf-8'))
  data = tcpCliSock.recv(BUFSIZ)
  if not data:
    break
  print(data.decode('utf-8'))

# The client side ends communication
tcpCliSock.close()
