import sys
import hashlib

#plaintext = open(sys.argv[2], "rb")
ciphertext = open(sys.argv[3], "wb")
password = sys.argv[1]
hash = 0


hasher = hashlib.sha256()
try:
    with open(sys.argv[2], "rb") as afile:
        buf = afile.read()
        hasher.update(buf)
    print(hasher.hexdigest())
except:
    print("Error")


for element in password:
    c = ord(element)
    hash = c + (hash << 6) + (hash << 16) - hash

x = hash
IV = list()

for i in range(16):
    x = (1103515245*x + 12345) % 256
    IV.append(x)

cipher = list()
end_reached = False

while not end_reached:
    prev = cipher
    cipher = list()
    temp = list()
    keystream = list()

    for i in range(16):         #read the textstream
        plaintext_byte = plaintext.read(1)
        if not plaintext_byte:      #add padding if end is reached
            for k in range(16 - i):
                if len(prev) == 0:      #XOR with IV
                    temp.append(IV[i + k] ^ (16 - i))
                else:                   #XOR with prev block
                    temp.append(prev[i + k] ^ (16 - i))
            end_reached = True
            break
        else:
            if len(prev) == 0:      #XOR with IV
                temp.append(IV[i] ^ sum(bytearray(plaintext_byte)))
            else:                   #XOR with prev block
                temp.append(prev[i] ^ sum(bytearray(plaintext_byte)))

    for i in range(16):
        if len(prev) == 0:      #XOR with IV
            temp.append(IV[i] ^ sum(bytearray(plaintext_byte)))
        else:                   #XOR with prev block
            temp.append(prev[i] ^ sum(bytearray(plaintext_byte)))

    for i in range(16):         #read the keystream
        x = (1103515245*x + 12345) % 256
        keystream.append(x)

    for i in range(16):         #shuffle bytes
        bottom = keystream[i] & 0xf
        top = keystream[i]>>4 & 0xf
        tempblock = temp[bottom]
        temp[bottom] = temp[top]
        temp[top] = tempblock

    for i in range(16):         #XOR with keystream and write
        cipher.append(keystream[i] ^ temp[i])
        ciphertext.write(cipher[i].to_bytes(1,'big'))


plaintext.close()
ciphertext.close()