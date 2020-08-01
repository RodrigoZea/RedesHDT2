# Laboratorio 2
# Integrantes
# Rodrigo Zea / 17058
# Miguel Valle / 17102

# Importing useful libraries
import bitarray
import pickle
import socket

ba = bitarray.bitarray()

""" SEND a message """
# Enter a message
userTxt = input("Ingrese un mensaje a enviar: ")
# Use bitarray to convert
ba.frombytes(userTxt.encode('utf-8'))
print(ba)
print(ba[0])

# Hamming Code
m = len(ba)

# Calculate redundant bits
# Use the formula: 2^r >= m + r + 1
for i in range(m):
    if (2**i >= m + i + 1):
        return i


# Add noise
# Send to socket
