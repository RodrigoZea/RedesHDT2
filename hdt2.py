# Laboratorio 2
# Integrantes
# Rodrigo Zea / 17058
# Miguel Valle / 17102

# Importing useful libraries
import bitarray
import pickle
import socket
import random

from numpy import random
BLOCK_SIZE = 8
MODULO = 255
OBJECT = {'message': [], 'check1': -1, 'check2': -1, 'arr':''}
HOST = 'localhost'
PORT = 50007


ba = bitarray.bitarray()

""" SEND a message """
# Enter a message
userTxt = input("Ingrese un mensaje a enviar: ")
# Use bitarray to convert
ba.frombytes(userTxt.encode('utf-8'))


"""Turn into list and prepare"""
l = ba.tolist()
baO = bitarray.bitarray()
baO = ba
temp = ['1' if x else '0' for x in l]
mod = len(temp) % BLOCK_SIZE
if (mod > 0):
    byteNum = (len(temp) // BLOCK_SIZE) + 1
else:
    byteNum = (len(temp) // BLOCK_SIZE)

"""FLETCHER CHECKSUM"""
str1 = ""
sum1 = 0;
sum2 = 0;
for i in range(byteNum):
    temporal = temp[i*BLOCK_SIZE:(i*BLOCK_SIZE)+BLOCK_SIZE]
    str1 = ""
    str1 = str1.join(temporal)
    sum1 = (sum1 + int(str1, 2)) % MODULO
    sum2 = (sum2 + sum1) % MODULO
check1 = MODULO - ((sum1 + sum2) % MODULO)
check2 = MODULO - ((sum1 + check1) % MODULO)
#OBJECT["message"] = ba
OBJECT["check1"] = check1
OBJECT["check2"] = check2
print("Checksum1: ",OBJECT["check1"])
print("Checksum2: ",OBJECT["check2"])

""" ADD NOISE """
noiseNum = "-1"
while (noiseNum.isnumeric() == False) or (int(noiseNum) > 100):
    try:
        noiseNum = input("Ingrese una num. entre 0 y 100 de ruido: ")
    except ValueError:
        print("No es un número válido")
        continue

for i in range(len(l)):
    x = random.randint(100)
    if(x < 30):
        l[i] = not(l[i])
ba = bitarray.bitarray(l)
l = ba.tolist()
temp = ['1' if x else '0' for x in l]

""" HAMMING CODE """
# Implementacion de: https://www.geeksforgeeks.org/hamming-code-implementation-in-python/
# Calculate redundant bits
# Use the formula: 2^r >= m + r + 1
def redBits(m):
    for i in range(m):
        if (2**i >= m + i + 1):
            return i


# Get position of redundant bits
# Los bits redundantes deberian estar en posiciones 2^n 
# Entonces empezamos buscando esas posiciones
def posRedundantBits(data, r): 
  
    # Redundancy bits are placed at the positions 
    # which correspond to the power of 2. 
    j = 0
    k = 1
    m = len(data) 
    res = '' 
  
    # If position is power of 2 then insert '0' 
    # Else append the data 
    for i in range(1, m + r+1): 
        if(i == 2**j): 
            res = res + '0'
            j += 1
        else: 
            res = res + data[-1 * k] 
            k += 1
  
    # The result is reversed since positions are 
    # counted backwards. (m + r+1 ... 1) 
    return res[::-1] 

def calcParityBits(arr, r): 
    n = len(arr) 
  
    # For finding rth parity bit, iterate over 
    # 0 to r - 1 
    for i in range(r): 
        val = 0
        for j in range(1, n + 1): 
  
            # If position has 1 in ith significant 
            # position then Bitwise OR the array value 
            # to find parity bit value. 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
                # -1 * j is given since array is reversed 
  
        # String Concatenation 
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n) 
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:] 
    return arr 
  
  
def detectError(arr, nr): 
    n = len(arr) 
    res = 0
  
    # Calculate parity bits again 
    for i in range(nr): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
  
        # Create a binary no by appending 
        # parity bits together. 
  
        res = res + val*(10**i) 
  
    # Convert binary to decimal 
    return int(str(res), 2) 
  
m = len(ba)

r = redBits(m)
OBJECT["message"] = ba
print("Bitarray original: ",baO)
print("Bitarray enviado: ",ba)
arr = posRedundantBits(temp, r)
arr = calcParityBits(arr, r)
print("Data transferida: " + arr)
print("Error data es: " + arr)
correction = detectError(arr, r)
print("La posicion del error es: " + str(correction))
data_string = pickle.dumps(OBJECT)
""" SEND to socket """
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(data_string)
s.close()
print ('Data sent to server')


