import socket, pickle,bitarray
BLOCK_SIZE = 8
MODULO = 255
HOST = 'localhost'
PORT = 50007

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

data = conn.recv(4096)
data_variable = pickle.loads(data)
conn.close()
print (data_variable)
print ('Data received from client')
ba = bitarray.bitarray()
ba = data_variable["message"]
l = ba.tolist()
print(l)
temp = ['1' if x else '0' for x in l]
"""Verificacion FLETCHER CHECKSUM"""
print(temp)
print(len(temp))
mod = len(temp) % BLOCK_SIZE
if (mod > 0):
    byteNum = (len(temp) // BLOCK_SIZE) + 1
    print(temp[byteNum])
else:
    byteNum = (len(temp) // BLOCK_SIZE)
str1 = ""
sum1 = 0;
sum2 = 0;
for i in range(byteNum):
    temporal = temp[i*BLOCK_SIZE:(i*BLOCK_SIZE)+BLOCK_SIZE]
    print(temporal)
    str1 = ""
    str1 = str1.join(temporal)
    sum1 = (sum1 + int(str1, 2)) % MODULO
    sum2 = (sum2 + sum1) % MODULO
check1 = MODULO - ((sum1 + sum2) % MODULO)
check2 = MODULO - ((sum1 + check1) % MODULO)
if((check1 != data_variable["check1"]) or (check2 != data_variable["check2"])):
   print("Se detecto que hay errores con FLETCHER CHECKSUM")
else:
    print("No se detectaron errores con FLETCHER CHECKSUM")
"""Verificacion Hamming Code"""
m = len(ba)

r = redBits(m)

arr = posRedundantBits(temp, r)
arr = calcParityBits(arr, r)
correction = detectError(arr, r)
print("Data transferida: " + arr)
print("Error data es: " + arr)
print("La posicion del error es: " + str(correction))
