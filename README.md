# Week 3: Homework 1: symmetric Key Cryptography : Challenge Response Project in Python

# 1. Set up environment

I will use MacOS.

make sure system has python3 and pip3

- install crypto related python package

```python
pip3 install pycryptodome
```

# 2. Encryption/Decryption with RC4

- create config.py

```python
HOST = '127.0.0.1'
PORT = 5001
BUFSIZ = 1024
ADDR = (HOST, PORT)
```

- create ctr.py

```python
#!/usr/bin/env python

import binascii

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random

# AES supports multiple key sizes: 16 (AES128), 24 (AES192), 
# or 32 (AES256).
key_bytes = 32
KEY = '12345678901234567890123456789012'

def encrypt(key, plaintext):
  assert len(key) == key_bytes

  # Choose a random, 16-byte IV.
  iv = Random.new().read(AES.block_size)

  # Convert the IV to a Python integer.
  iv_int = int(binascii.hexlify(iv), 16)

  # Create a new Counter object with IV = iv_int.
  ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

  # Create AES-CTR cipher.
  aes = AES.new(key.encode('utf-8'), mode=AES.MODE_CTR, counter=ctr)

  # Encrypt and return IV and ciphertext.
  ciphertext = aes.encrypt(plaintext.encode('utf-8'))
  return (iv, ciphertext)

def decrypt(key, iv, ciphertext):
  assert len(key) == key_bytes

  # Initialize counter for decryption. iv should be
  # the same as the output of encrypt().
  iv_int = int(iv.hex(), 16)
  ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
  # iv = "0000000000000000".encode("utf-8")
  # Create AES-CTR cipher.
  aes = AES.new(key.encode('utf-8'), mode=AES.MODE_CTR, counter=ctr)

  # Decrypt and return the plaintext.
  plaintext = aes.decrypt(ciphertext)
  return plaintext
```

- create server.py

```python
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
```

- create client.py

```python
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
```

- start server

```python
python3 server.py
```

- start client

```python
python3 client.py
```

- Type ‘Hello World’
- Result

![Untitled](Week%203%20Homework%201%20symmetric%20Key%20Cryptography%20Chall%20f3df3f00d41249948003e5e0317ff8dd/Untitled.png)