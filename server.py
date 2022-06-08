#!/usr/bin/env python

import binascii
import sys

from random import randint
from socket import *
from time import ctime

from ctr import decrypt, encrypt, KEY
from config import HOST, PORT, BUFSIZ, ADDR

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
  print('socket bound to address {} and port {}'.format(HOST, PORT))
  tcpCliSock, addr = tcpSerSock.accept()
  print('Accepted connection from host {} and port {}'.format(addr[0], addr[1]))

  data = tcpCliSock.recv(BUFSIZ)
  randomValue = int(data.decode('utf-8'))
  print("Get A random number {} from the client.".format(randomValue))

  temp = encrypt(KEY, str(randomValue))
  print("Encrypted plain text {} ==> {}".format(randomValue, temp))

  print("Wrote back to the client.")
  tcpCliSock.send(temp[0])
  data = tcpCliSock.recv(BUFSIZ)
  tcpCliSock.send(temp[1])

  while True:
    data = tcpCliSock.recv(BUFSIZ)
    # For example, if the client side
    # type Return without entering any
    # message to end communication.
    if not data:
      break
    timeWithData = "[" + ctime() + "] " + data.decode('utf-8')
    tcpCliSock.send(timeWithData.encode('utf-8'))

  # The client side ends communication
  tcpCliSock.close()
# The server side ends communication
tcpSerSock.close()
