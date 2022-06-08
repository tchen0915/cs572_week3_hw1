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
