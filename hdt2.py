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
# Hamming Code
# Add noise
# Send to socket
